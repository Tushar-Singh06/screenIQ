import json
import re

from groq import Groq
from django.conf import settings

from .prompts import SCREENING_PROMPT
from .utils import normalize_score


client = Groq(api_key=settings.GROQ_API_KEY)


class AIService:

    @staticmethod
    def extract_json(content):

        # Extract JSON block safely
        match = re.search(r'\{.*\}', content, re.DOTALL)

        if not match:
            raise Exception("No valid JSON found in AI response")

        return json.loads(match.group())

    @staticmethod
    def screen_candidate(job_description, resume):

        prompt = SCREENING_PROMPT.format(
            job_description=job_description,
            resume=resume
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = completion.choices[0].message.content

        parsed = AIService.extract_json(content)

        score = normalize_score(parsed.get("score", 0))

        reasons = parsed.get("reasons", [])

        return {
            "score": score,
            "reasons": reasons
        }