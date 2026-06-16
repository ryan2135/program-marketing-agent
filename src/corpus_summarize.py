import requests
from pathlib import Path

corpus_name = input("Corpus file name (without -corpus.txt): ")

corpus_path = Path(f"outputs/{corpus_name}-corpus.txt")
summary_path = Path(f"outputs/{corpus_name}-summary.txt")

corpus = corpus_path.read_text(encoding="utf-8")

sections = corpus.split("=" * 80)

with open(summary_path, "w", encoding="utf-8") as out:

    for i, section in enumerate(sections):

        section = section.strip()

        if len(section) < 200:
            continue

        print(f"Summarizing section {i}")

        prompt = f"""
Summarize this page in 5 bullet points for a university recruiting application.

PAGE:

{section[:6000]}
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

        out.write("\n")
        out.write("#" * 60)
        out.write("\n")

        out.write(data.get("response", "ERROR"))
        out.write("\n\n")

print(f"Saved summaries to {summary_path}")