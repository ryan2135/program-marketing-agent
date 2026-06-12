import requests

url = "https://www.pacificu.edu/computer-science"

response = requests.get(url)

print("Status:", response.status_code)
print("Characters:", len(response.text))

with open("outputs/computer-science.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Saved: outputs/computer-science.html")