import requests
from pathlib import Path

MODEL = "hf.co/ggml-org/gemma-4-12B-it-GGUF:Q4_K_M"


def clean_llm_output(text):
    text = text.replace("<|channel>thought", "")
    text = text.replace("<channel|>", "")
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


program_name = input("Program name: ")

summary_path = Path(f"outputs/{program_name}-summary.txt")
stories_path = Path(f"outputs/{program_name}-stories.json")

summary = summary_path.read_text(encoding="utf-8")

prompt = f"""
Use the source material below to extract content for two app sections:

1. Featured Student Stories
2. Student Showcase

Use ONLY facts supported by the source material.

Return ONLY valid JSON with this structure:

{{
  "featured_stories": [
    {{
      "title": "",
      "summary": "",
      "story_type": "",
      "source_evidence": ""
    }}
  ],
  "showcase_cards": [
    {{
      "title": "",
      "summary": "",
      "card_type": "",
      "source_evidence": ""
    }}
  ]
}}

Rules for featured_stories:
- Extract up to 3 stories.
- Prefer real named students, alumni, or recent graduates.
- Focus on human journeys, accomplishments, challenges, and outcomes.
- Do not invent names, employers, projects, or outcomes.
- Return fewer than 5 if the source does not support 5.

Rules for showcase_cards:
- Extract up to 6 cards.
- Prefer concrete experiences: projects, practicums, internships, research, presentations, performances, field placements, community work, capstones, clubs, or pathways.
- Avoid accreditation, admissions requirements, generic curriculum, and administrative facts unless there are not enough stronger items.
- Focus on what students actually do or experience.
- Do not invent details.

Do not include markdown.

SOURCE MATERIAL:

{summary}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    },
)

data = response.json()

generated_text = clean_llm_output(data.get("response", ""))

stories_path.write_text(generated_text, encoding="utf-8")

print(f"Saved stories to {stories_path}")