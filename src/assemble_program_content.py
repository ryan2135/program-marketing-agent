import json
from pathlib import Path


def assemble_program_content(program_name):

    facts_path = Path(f"outputs/{program_name}.json")
    marketing_path = Path(f"outputs/{program_name}-marketing.json")
    stories_path = Path(f"outputs/{program_name}-stories.json")
    app_path = Path(f"outputs/{program_name}-app.json")

    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    marketing = json.loads(marketing_path.read_text(encoding="utf-8"))
    stories = json.loads(stories_path.read_text(encoding="utf-8"))

    app = {
        "hero": {
            "program_name": facts.get("program_name"),
            "degree_type": facts.get("degree_type"),
            "location": facts.get("location"),
            "format": facts.get("format"),
            "tagline": marketing.get("tagline"),
            "overview": marketing.get("overview"),
        },
        "why_students_choose": marketing.get("why_study", []),
        "featured_student_stories": stories.get("featured_stories", []),
        "student_showcase": stories.get("showcase_cards", []),
        "career_paths": marketing.get("career_paths", []),
        "faculty_mentors": marketing.get("faculty_highlights", []),
        "apply_request_info": {
            "label": "Apply or request information",
            "note": "Connect with admissions to learn more about this program.",
        },
    }

    app_path.write_text(
        json.dumps(app, indent=2),
        encoding="utf-8"
    )

    print(f"Saved app JSON to {app_path}")


if __name__ == "__main__":
    program_name = input("Program name: ")
    assemble_program_content(program_name)