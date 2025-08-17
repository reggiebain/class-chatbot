import os
from openai import OpenAI
from langchain.chains import OpenAIModerationChain
from config import OPENAI_API_KEY

class ModerationService:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY
        if not api_key:
            raise ValueError("No OpenAI API key provided or found")
        self.client = OpenAI(api_key=api_key)
        self.chain = OpenAIModerationChain()  # optional, can still use client for full metadata

    def check(self, text: str) -> tuple[dict, dict]:
        """
        Run moderation on text and return:
            - normalized: {"flagged": bool, "categories": dict}
            - raw: raw OpenAI moderation API result
        """
        try:
            # Direct call to OpenAI moderation for full metadata
            raw_result = self.client.moderations.create(
                model="omni-moderation-latest",
                input=text
            ).results[0]

            # Convert categories object to dict safely
            if hasattr(raw_result.categories, "__dict__"):
                categories_dict = {k: v for k, v in vars(raw_result.categories).items() if v}
            else:
                categories_dict = dict(raw_result.categories) if raw_result.categories else {}

            normalized = {
                "flagged": raw_result.flagged,
                "categories": categories_dict,
            }

            # Convert raw_result to dict for logging
            raw = vars(raw_result)

            return normalized, raw

        except Exception as e:
            print(f"Moderation failed: {e}")
            return {"flagged": False, "categories": {}}, {}
