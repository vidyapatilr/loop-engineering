"""The Reviewer: critiques the Builder's latest HTML against a rubric and returns a verdict.
Per the article, the Reviewer never edits or rewrites the HTML itself — it only ever gives
feedback back to the Builder. It also runs on a different model family than the Builder
(see client.py) so it isn't grading output produced by its own model."""

import re

from loop_builder.client import REVIEWER_MODEL, client

SYSTEM_PROMPT = """You are the Reviewer in a two-agent content loop. You never write or edit \
HTML yourself — you only critique what the Builder produced and decide whether it's ready.

Judge the HTML against this rubric:
- Clarity: would a non-technical reader understand it without help?
- Concrete example: does it include at least one worked example, not just abstract description?
- Visual aid: is there at least one simple diagram (inline SVG, CSS, or similar)?
- No unexplained jargon: any technical term either isn't used, or is explained in plain words.
- Accuracy: nothing in the RESEARCH_NOTES the Builder flagged should be left unresolved or
  contradicted by the page itself.

Be specific and actionable in feedback — name what's missing or wrong, not just that something
"could be better." Do not rewrite or suggest exact replacement text; describe the problem so the
Builder can fix it.

Output ONLY in this exact format, nothing else before or after:
VERDICT: APPROVE or REVISE
FEEDBACK:
- <specific point>
- <specific point>
(If VERDICT is APPROVE, FEEDBACK may be a single line noting it meets the rubric.)"""


def _build_user_prompt(goal: str, html: str, iteration: int, max_iterations: int) -> str:
    return (
        f"GOAL:\n{goal}\n\n"
        f"This is iteration {iteration} of a maximum of {max_iterations}.\n\n"
        f"Here is the HTML to review:\n\n{html}"
    )


def _parse(raw: str) -> dict:
    verdict_match = re.search(r"VERDICT:\s*(APPROVE|REVISE)", raw)
    feedback_match = re.search(r"FEEDBACK:\s*(.+)", raw, re.DOTALL)

    if not verdict_match:
        raise ValueError("Reviewer output did not contain a parseable VERDICT:\n" + raw[:500])

    return {
        "verdict": verdict_match.group(1).strip(),
        "feedback": feedback_match.group(1).strip() if feedback_match else "none",
    }


def review(goal: str, html: str, iteration: int, max_iterations: int) -> dict:
    response = client.chat.completions.create(
        model=REVIEWER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(goal, html, iteration, max_iterations)},
        ],
    )
    return _parse(response.choices[0].message.content)
