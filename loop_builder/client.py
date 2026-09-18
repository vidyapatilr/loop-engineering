"""We deliberately point Builder and Reviewer at two different model families so the
Reviewer is never grading output produced by its own model (avoids self-grading bias)."""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

BUILDER_MODEL = "openai/gpt-4o-mini"
REVIEWER_MODEL = "anthropic/claude-3-haiku"
