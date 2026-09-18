"""Two persistent logs carried across iterations: a research log (claims/sources used) and a change log (what changed and why).
Keeping these as plain files (not stuffed back into every prompt in full) is the offload-to-disk
technique — each iteration reads only what it needs from them."""

from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
RESEARCH_LOG = LOG_DIR / "research_log.md"
CHANGE_LOG = LOG_DIR / "change_log.md"


def init_logs():
    LOG_DIR.mkdir(exist_ok=True)
    if not RESEARCH_LOG.exists():
        RESEARCH_LOG.write_text(
            "# Research Log\n\nClaims and sources used while building the site.\n\n"
        )
    if not CHANGE_LOG.exists():
        CHANGE_LOG.write_text(
            "# Change Log\n\nWhat changed each iteration, and why.\n\n"
        )


def append_research(iteration: int, notes: str):
    if not notes or notes.strip().lower() == "none":
        return
    with RESEARCH_LOG.open("a") as f:
        f.write(f"## Iteration {iteration}\n{notes.strip()}\n\n")


def append_change(iteration: int, summary: str, verdict: str, feedback: str):
    with CHANGE_LOG.open("a") as f:
        f.write(f"## Iteration {iteration}\n")
        f.write(f"**Change:** {summary.strip()}\n\n")
        f.write(f"**Reviewer verdict:** {verdict}\n\n")
        if feedback and feedback.strip().lower() != "none":
            f.write(f"**Reviewer feedback:**\n{feedback.strip()}\n\n")


def read_change_log() -> str:
    return CHANGE_LOG.read_text() if CHANGE_LOG.exists() else ""
