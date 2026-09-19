# loop-engineering

A minimal Builder/Reviewer verification loop, built to explore "loop engineering" — using a second, independent LLM as an automated judge inside an agentic loop, and where that judge can quietly fail.

The loop writes a single self-contained HTML page that explains what an agent loop is to a non-technical reader. That's the test task; the actual subject of this repo is the loop itself, and what went wrong while building it. The full write-up of the failures below is in the companion LinkedIn post 
[https://www.linkedin.com/feed/update/urn:li:activity:7507130824484589568/].

## How it works

1. **Builder** (`loop_builder/builder.py`) writes the page on iteration 1, or revises it on later iterations based on the Reviewer's feedback.
2. **Reviewer** (`loop_builder/reviewer.py`) reads that same HTML and returns `APPROVE` or `REVISE` + specific feedback, judged against a rubric. It never edits the page itself.
3. On `REVISE`, the feedback is fed back into the next Builder call.
4. The loop stops on `APPROVE`, or after **5 iterations** (`MAX_ITERATIONS`) — whichever comes first. Hitting the cap without approval is treated as a guardrail firing, not a silent success.

Builder and Reviewer run on two different model families (`loop_builder/client.py`) — the Reviewer is never grading output from its own model family, to avoid self-grading bias.

| Role | Model |
|------|-------|
| Builder | `openai/gpt-4o-mini` |
| Reviewer | `anthropic/claude-3-haiku` |

Both are called through [OpenRouter](https://openrouter.ai/), so you only need one API key regardless of which models you swap in.

## What you get out of a run

- `site/index.html` — the final approved (or last) page.
- `iterations/iteration_N/` — a full trace per pass: the HTML at that point, the Builder's change summary, and the Reviewer's verdict + feedback.
- `logs/research_log.md` — claims/sources the Builder flagged as worth double-checking, across the whole run.
- `logs/change_log.md` — what changed each iteration, and the Reviewer's response to it.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <this-repo-url>
cd loop-engineering
uv sync
cp .env.example .env
# then add your OpenRouter key to .env:
# OPENROUTER_API_KEY=sk-or-...
```

Get a key at [openrouter.ai](https://openrouter.ai/).

## Run it

```bash
uv run python -m loop_builder.run_loop
```

Progress prints per iteration (Builder's change summary, Reviewer's verdict). When it finishes, open `site/index.html`.

## Why this exists

This started as a straightforward "Builder writes, Reviewer checks" demo. What made it worth publishing were the ways the Reviewer's approval turned out not to mean what it looked like it meant — a rubric that only checked "is there an example?" approving an example that wasn't actually one, a Reviewer that described verifying things it had no way to verify from text alone, and a diagram that no amount of iteration could fix because neither agent could ever see it rendered. Those findings, and what I changed because of them, are written up in the linked post — this repo is the thing that produced them.
