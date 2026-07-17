import argparse
import requests
import xml.etree.ElementTree as ET


def download_image(url: str, path: str) -> None:
    response = requests.get(url)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)


def fetch_films_text(rss_url: str) -> str:
    response = requests.get(rss_url)
    response.raise_for_status()

    # Get first item in the feed
    root = ET.fromstring(response.text)
    item = root.find("channel/item")
    title = item.find("title").text
    link = item.find("link").text

    # Try to get the image URL
    description = item.find("description").text
    img_url = description.split('<img src="')[1].split('"')[0]
    title_text = f"[{title}]({link})"
    img_text = f'<img src="{img_url}" alt="{title}" width="100" height="150" />'
    return f"{title_text}\n\n{img_text}"


def update_readme(path: str, replace: dict[str, str]) -> None:
    with open(path, "r") as file:
        text = file.read()

    # Find start and end markers
    for key, value in replace.items():
        start_marker = f"<!-- START_SECTION:{key} -->"
        end_marker = f"<!-- END_SECTION:{key} -->"
        start_index = text.find(start_marker)
        end_index = text.find(end_marker)
        text = (
            text[:start_index] + text[start_index:end_index] + value + text[end_index:]
        )

    with open(path, "w") as file:
        file.write(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="README.md")
    args = parser.parse_args()
    update_readme(
        args.path,
        {
            "films": fetch_films_text("https://letterboxd.com/pdeziel/rss/"),
        },
    )
