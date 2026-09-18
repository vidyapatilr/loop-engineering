"""The Builder: produces the first draft, then revises based on Reviewer feedback each pass.
Builder never grades its own work — it only ever writes, and the loop's stopping decision is
made entirely by the (separate-model) Reviewer in reviewer.py."""

import re

from loop_builder.client import BUILDER_MODEL, client

SYSTEM_PROMPT = """You are the Builder in a two-agent content loop. You write a single, \
self-contained HTML file (inline CSS and JS only, no external assets) that explains a topic \
clearly to a non-technical reader.

Rules:
- Output ONLY in the exact format below, nothing else before or after.
- The HTML must be complete and valid, starting with <!doctype html>.
- Do not include markdown code fences anywhere in your output.
- Keep language plain; avoid unexplained jargon.
- If you use a fact or claim you want double-checked, add a line for it in RESEARCH_NOTES.

Output format (follow exactly):
CHANGE_SUMMARY: <one or two sentences on what you wrote or changed this pass, and why>
RESEARCH_NOTES: <bullet list of claims worth double-checking, or 'none'>
---HTML START---
<the full html document>
---HTML END---"""


def _build_user_prompt(
    goal: str, current_html: str | None, reviewer_feedback: str | None, iteration: int
) -> str:
    parts = [f"GOAL:\n{goal}\n"]
    if current_html is None:
        parts.append("This is iteration 1. Write the first draft from scratch.")
    else:
        parts.append(
            f"This is iteration {iteration}. Here is the current HTML:\n\n{current_html}\n"
        )
        parts.append(
            f"Here is the Reviewer's feedback from the last pass — address it directly:\n\n{reviewer_feedback}\n"
        )
    return "\n".join(parts)


def _parse(raw: str) -> dict:
    change_match = re.search(
        r"CHANGE_SUMMARY:\s*(.+?)(?=RESEARCH_NOTES:)", raw, re.DOTALL
    )
    notes_match = re.search(
        r"RESEARCH_NOTES:\s*(.+?)(?=---HTML START---)", raw, re.DOTALL
    )
    html_match = re.search(r"---HTML START---\s*(.+?)\s*---HTML END---", raw, re.DOTALL)

    if not html_match:
        raise ValueError(
            "Builder output did not contain a parseable HTML block:\n" + raw[:500]
        )

    return {
        "change_summary": change_match.group(1).strip()
        if change_match
        else "(no summary given)",
        "research_notes": notes_match.group(1).strip() if notes_match else "none",
        "html": html_match.group(1).strip(),
    }


def build(
    goal: str, current_html: str | None, reviewer_feedback: str | None, iteration: int
) -> dict:
    response = client.chat.completions.create(
        model=BUILDER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": _build_user_prompt(
                    goal, current_html, reviewer_feedback, iteration
                ),
            },
        ],
    )
    return _parse(response.choices[0].message.content)
