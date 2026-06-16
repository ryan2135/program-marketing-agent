import json
import requests
from pathlib import Path

input_name = input("Corpus file name without '-corpus.txt': ")

corpus_path = Path(f"outputs/{input_name}-corpus.txt")
output_path = Path(f"outputs/{input_name}-marketing.json")

corpus = corpus_path.read_text(encoding="utf-8")[:10000]

prompt = f"""
Use the source material below to create recruiting content for a mobile-friendly academic program app.

Return ONLY valid JSON with these keys:
program_name
tagline
overview
why_study
career_paths
student_story_ideas
faculty_highlights
app_sections

SOURCE MATERIAL:
{corpus}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "hf.co/ggml-org/gemma-4-12B-it-GGUF:Q4_K_M",
        "prompt": prompt,
        "stream": False,
    },
)

data = response.json()
print(data.keys())
generated_text = data["response"]

output_path.write_text(generated_text, encoding="utf-8")

print(f"Saved marketing JSON to {output_path}")