import requests
from bs4 import BeautifulSoup

base_url = "https://sv.wikipedia.org"
start_url = base_url + "/wiki/Portal:Huvudsida"  # Startsidan


def fetch_wiki_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    wiki_links = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("/wiki/") and ":" not in href:
            wiki_links.append(base_url + href)

    return wiki_links


def crawl_wiki(start, max_links, output_file):
    visited = set()
    queue = [start]
    link_count = 0

    with open(output_file, "w") as file:
        while queue and link_count < max_links:
            current_url = queue.pop(0)
            if current_url not in visited:
                print("Hämtar länkar från:", current_url)
                visited.add(current_url)
                links = fetch_wiki_links(current_url)
                queue.extend(links)
                link_count += 1
                file.write(current_url + "\n")


crawl_wiki(start_url, 1000, "lista_urler.txt")
