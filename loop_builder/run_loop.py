"""Orchestrates the Builder/Reviewer loop:
  1. Builder writes (iteration 1) or revises (later iterations) the HTML.
  2. Reviewer critiques that same HTML and returns APPROVE or REVISE + feedback.
  3. On REVISE, the Reviewer's feedback is fed back into the next Builder call.
  4. Stops on APPROVE, or when MAX_ITERATIONS is hit (the guardrail) — whichever comes first.

Every iteration is saved to iterations/iteration_N/ (a full trace), the working page is written
to site/index.html each pass, and the two logs (research_log.md, change_log.md) are updated.
"""

from pathlib import Path

from loop_builder.builder import build
from loop_builder.logs import append_change, append_research, init_logs
from loop_builder.reviewer import review

GOAL = """Build a single, self-contained HTML page that explains "agent loops" to a
non-technical reader: what a loop is (send context to a model, run any tool calls it asks
for, append the results, repeat until done or a stopping condition is hit), why you'd want
one instead of a single request, and what can go wrong if it isn't designed carefully
(runaway cost, losing track of context, no way to verify the output).

For the diagram, keep it simple: a single bordered box containing one bold line of text
showing the stage names separated by arrows, e.g. "Context -> Model Response -> Actions
Taken -> Updated Context -> Repeat". Do not use SVG, shapes, or multi-box graphics for the
diagram - a styled text line is all that's needed. Style the diagram box to fit its content 
width rather than stretching across the full page, and left-align the text inside it.

The page must include a concrete worked example with a specific, realistic scenario (an
actual question, actual numbers or data, an actual tool being called and a specific result
it returns) - not a restatement of the abstract stage names from the diagram or definition.
Present it as numbered steps (1, 2, 3...). This example is required in every draft,
including revisions - never drop it while making other changes.

Do not include site-wide boilerplate that doesn't serve the explanation - no fake
copyright notice, no placeholder navigation bar, no "About Us" or contact footer."""

MAX_ITERATIONS = 5

ROOT = Path(__file__).parent.parent
SITE_FILE = ROOT / "site" / "index.html"
ITERATIONS_DIR = ROOT / "iterations"


def _save_iteration(
    n: int, html: str, change_summary: str, verdict: str, feedback: str
):
    iter_dir = ITERATIONS_DIR / f"iteration_{n}"
    iter_dir.mkdir(parents=True, exist_ok=True)
    (iter_dir / "index.html").write_text(html)
    (iter_dir / "change_summary.txt").write_text(change_summary)
    (iter_dir / "reviewer_verdict.txt").write_text(
        f"VERDICT: {verdict}\n\nFEEDBACK:\n{feedback}"
    )


def run():
    init_logs()

    current_html = None
    reviewer_feedback = None

    print("=" * 60)
    print("Loop Engineering Demo — Builder/Reviewer loop")
    print("=" * 60)

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")

        print("Builder writing...")
        builder_result = build(GOAL, current_html, reviewer_feedback, iteration)
        current_html = builder_result["html"]
        print(f"  Change: {builder_result['change_summary']}")

        SITE_FILE.write_text(current_html)

        print("Reviewer reviewing...")
        review_result = review(GOAL, current_html, iteration, MAX_ITERATIONS)
        verdict = review_result["verdict"]
        reviewer_feedback = review_result["feedback"]
        print(f"  Verdict: {verdict}")
        print(f"  Feedback: {reviewer_feedback[:200]}")

        _save_iteration(
            iteration,
            current_html,
            builder_result["change_summary"],
            verdict,
            reviewer_feedback,
        )
        append_research(iteration, builder_result["research_notes"])
        append_change(
            iteration, builder_result["change_summary"], verdict, reviewer_feedback
        )

        if verdict == "APPROVE":
            print(f"\nApproved after {iteration} iteration(s). Final page: {SITE_FILE}")
            break
    else:
        print(
            f"\nHit the {MAX_ITERATIONS}-iteration cap without approval. Final page: {SITE_FILE}"
        )
        print(
            "(This is the guardrail working as intended — a real project might flag this"
        )
        print("for a human rather than silently accepting the last draft.)")


if __name__ == "__main__":
    run()
