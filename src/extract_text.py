import requests
from bs4 import BeautifulSoup
from pathlib import Path

url = input("URL: ")
output_name = input("Output file name (without extension): ")

html_path = Path(f"outputs/{output_name}.html")
text_path = Path(f"outputs/{output_name}.txt")

response = requests.get(url)

if response.status_code != 200:
    print(f"Error: HTTP {response.status_code}")
    exit(1)

html = response.text

html_path.write_text(html, encoding="utf-8")

soup = BeautifulSoup(html, "html.parser")

for tag in soup(["script", "style", "nav", "footer", "header"]):
    tag.decompose()

text = soup.get_text(separator="\n")

lines = []

for line in text.splitlines():
    line = line.strip()

    if line:
        lines.append(line)

clean_text = "\n".join(lines)

text_path.write_text(clean_text, encoding="utf-8")

print(f"Saved HTML: {html_path}")
print(f"Saved Text: {text_path}")