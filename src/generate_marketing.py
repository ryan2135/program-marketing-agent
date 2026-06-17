import requests
from pathlib import Path

MODEL = "hf.co/ggml-org/gemma-4-12B-it-GGUF:Q4_K_M"


def clean_llm_output(text):
    text = text.replace("<|channel>thought", "")
    text = text.replace("<channel|>", "")
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


input_name = input("Program name: ")

summary_path = Path(f"outputs/{input_name}-summary.txt")
output_path = Path(f"outputs/{input_name}-marketing.json")

summary = summary_path.read_text(encoding="utf-8")

prompt = f"""
Use the source material below to create recruiting content for a mobile-friendly academic program app.

IMPORTANT:
- Use ONLY facts supported by the source material.
- Do NOT invent companies, technologies, courses, faculty accomplishments, travel opportunities, or career outcomes.
- If information is unavailable, omit it.
- Return ONLY valid JSON.
- Do not include explanations.
- Do not include markdown.

Return ONLY valid JSON with this structure:

{{
  "program_name": "",
  "tagline": "",
  "overview": "",
  "why_study": [],
  "career_paths": [],
  "student_story_ideas": [],
  "faculty_highlights": [],
  "app_sections": []
}}

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

generated_text = clean_llm_output(
    data.get("response", "")
)

output_path.write_text(
    generated_text,
    encoding="utf-8"
)

print(f"Saved marketing JSON to {output_path}")