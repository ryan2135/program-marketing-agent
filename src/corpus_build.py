import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse


def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def build_corpus(program_url, output_name):
    corpus_path = Path(f"outputs/{output_name}-corpus.txt")

    response = requests.get(program_url)

    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(program_url, href)

        if "pacificu.edu" in urlparse(full_url).netloc:
            links.append(full_url)

    unique_links = sorted(set(links))

    useful_keywords = [
        output_name,
        "magazine",
        "accreditation",
        "catalog",
    ]

    filtered_links = []

    for link in unique_links:
        if any(keyword in link for keyword in useful_keywords):
            filtered_links.append(link)

    with open(corpus_path, "w", encoding="utf-8") as corpus:

        for link in filtered_links:

            print(f"Processing: {link}")

            try:
                response = requests.get(link, timeout=10)

                if response.status_code != 200:
                    continue

                clean_text = extract_visible_text(response.text)

                corpus.write("\n")
                corpus.write("=" * 80)
                corpus.write("\n")
                corpus.write(link)
                corpus.write("\n")
                corpus.write("=" * 80)
                corpus.write("\n\n")
                corpus.write(clean_text)
                corpus.write("\n\n")

            except Exception as e:
                print(f"Error: {e}")

    print(f"\nSaved corpus to {corpus_path}")


if __name__ == "__main__":
    program_url = input("Program URL: ")
    output_name = input("Corpus file name (without extension): ")

    build_corpus(program_url, output_name)