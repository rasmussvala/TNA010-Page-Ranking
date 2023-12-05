import requests


def get_all_pages_from_wiki(language_code, output_file):
    base_url = f"https://{language_code}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit": "max",  # Retrieves maximum number of pages per request
    }

    all_pages = set()
    continue_param = None
    total_pages = 0
    target_pages = 100000  # Change to desired target

    while total_pages < target_pages:
        if continue_param:
            params["apcontinue"] = continue_param

        response = requests.get(base_url, params=params)
        data = response.json()

        for page in data["query"]["allpages"]:
            # Check if 'title' exists in the dictionary before adding
            if "title" in page:
                # Construct full URL and add to the set
                full_url = f"https://{language_code}.wikipedia.org/wiki/{page['title'].replace(' ', '_')}"
                all_pages.add(full_url)
                total_pages += 1

                if total_pages >= target_pages:
                    break

        print(
            f"Pages retrieved: {total_pages}/{target_pages}", end="\r"
        )  # Update progress

        if "continue" in data and total_pages < target_pages:
            continue_param = data["continue"]["apcontinue"]
        else:
            break

    # Write URLs to output file
    with open(output_file, "w", encoding="utf-8") as file:
        for url in all_pages:
            file.write(url + "\n")

    print(f"\nStopped at {target_pages} pages. URLs saved to file.")


# Replace 'sv' with the appropriate language code
get_all_pages_from_wiki("sv", "sv_wiki_links.txt")
