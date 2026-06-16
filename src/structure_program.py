import json
from pathlib import Path

input_name = input("Input text file name (without extension): ")

input_path = Path(f"outputs/{input_name}.txt")
output_path = Path(f"outputs/{input_name}.json")

lines = input_path.read_text(encoding="utf-8").splitlines()


def value_after(label):
    if label in lines:
        index = lines.index(label)
        if index + 1 < len(lines):
            return lines[index + 1]
    return None


program = {
    "program_name": value_after("Text Box"),
    "degree_type": value_after("Degree Type"),
    "major_credits": value_after("Major Credits"),
    "minor_credits": value_after("Minor Credits"),
    "location": value_after("Location"),
    "format": value_after("Format"),
    "source_text_file": str(input_path),
}

output_path.write_text(
    json.dumps(program, indent=2),
    encoding="utf-8"
)

print(json.dumps(program, indent=2))