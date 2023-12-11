# WIP

import requests
import concurrent.futures


def fetch_backlinks(page_id, page_title):
    base_url = f"https://en.wikipedia.org/w/api.php"
    params_backlinks = {
        "action": "query",
        "format": "json",
        "list": "backlinks",
        "bltitle": page_title.replace(" ", "_"),
        "bllimit": "max",
    }

    response = requests.get(base_url, params=params_backlinks)
    data_backlinks = response.json()

    backlink_titles = [
        backlink["title"] for backlink in data_backlinks["query"]["backlinks"]
    ]
    return [(page_title, bl) for bl in backlink_titles]


def get_pages_and_backlinks(language_code, output_file):
    base_url = f"https://{language_code}.wikipedia.org/w/api.php"
    params_pages = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit": "max",
    }

    all_pages = {}
    total_pages = 0
    target_pages = 5000

    print("Fetching pages...")
    while total_pages < target_pages:
        params_pages["apcontinue"] = all_pages.get("continue", "")

        response_pages = requests.get(base_url, params=params_pages)
        data_pages = response_pages.json()

        for page in data_pages["query"]["allpages"]:
            all_pages[page["pageid"]] = page["title"]
            total_pages += 1

            if total_pages >= target_pages:
                break

        print(
            f"Pages fetched: {total_pages}/{target_pages}", end="\r"
        )  # Update progress

        if "continue" not in data_pages or total_pages >= target_pages:
            break

    print("\nFetching backlinks...")

    all_backlinks = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_page = {
            executor.submit(fetch_backlinks, page_id, page_title): (page_id, page_title)
            for page_id, page_title in all_pages.items()
        }
        for future in concurrent.futures.as_completed(future_to_page):
            page_id, page_title = future_to_page[future]
            try:
                backlinks = future.result()
                all_backlinks.extend(backlinks)
            except Exception as exc:
                print(
                    f"Fetching backlinks for {page_title} generated an exception: {exc}"
                )

    with open(output_file, "w", encoding="utf-8") as file:
        for idx, page_id in enumerate(all_pages):
            file.write(
                f"n {idx} https://{language_code}.wikipedia.org/wiki/{all_pages[page_id].replace(' ', '_')}\n"
            )

        for idx, (src, dst) in enumerate(all_backlinks):
            src_id = [idx for idx, title in all_pages.items() if title == src][0]
            dst_id = [idx for idx, title in all_pages.items() if title == dst][0]
            file.write(f"e {src_id} {dst_id}\n")

    print(
        f"\nDataset generated with {len(all_pages)} nodes and {len(all_backlinks)} edges."
    )


# Replace 'sv' with the appropriate language code
get_pages_and_backlinks("sv", "sv_wiki_dataset.txt")
