import json

from corpus_build import build_corpus
from corpus_summarize import summarize_corpus
from generate_marketing import generate_marketing


with open("inputs/programs.json", "r", encoding="utf-8") as f:
    programs = json.load(f)

for program in programs:

    name = program["name"]
    url = program["url"]

    answer = input(f"Run pipeline for {name}? (y/n): ")

    if answer.lower() != "y":
        continue

    print(f"\n=== Building corpus for {name} ===")
    build_corpus(url, name)

    print(f"\n=== Summarizing corpus for {name} ===")
    summarize_corpus(name)

    print(f"\n=== Generating marketing JSON for {name} ===")
    generate_marketing(name)

    print(f"\n=== Finished {name} ===\n")