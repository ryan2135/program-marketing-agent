import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = input("Program URL: ")

response = requests.get(url)

if response.status_code != 200:
    print(f"Error: HTTP {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

links = []

for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    full_url = urljoin(url, href)

    if "pacificu.edu" in urlparse(full_url).netloc:
        links.append(full_url)

unique_links = sorted(set(links))

useful_keywords = [
    "social-work",
    "magazine",
    "accreditation",
    "catalog",
    "claire-argow",
]

filtered_links = []

for link in unique_links:
    if any(keyword in link for keyword in useful_keywords):
        filtered_links.append(link)

print("\nUseful Links:\n")

for link in filtered_links:
    print(link)