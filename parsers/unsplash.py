import json
import requests


def search_on_unsplash(name, count):
    """
    Searches name on unsplash.com and parse image urls
    :return dict image urls
    """
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
    }

    page_counter = 1
    image_count = 0
    res = []
    while image_count < count:
        url = f"https://unsplash.com/napi/search/photos?" \
              f"query={name}&" \
              f"per_page=20&page={page_counter}"
        try:
            req = requests.get(url=url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?
        data = json.loads(req.text)

        for item in data['results']:
            image_link = item["urls"]["full"]

            if "plus.unsplash" in image_link:
                continue

            res.append(image_link)

            image_count += 1
            if image_count >= count:
                break
        page_counter += 1
    return res
