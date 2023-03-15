import requests
import os
import json
import httplib2

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
}

query = {
    "train": 36,
    "ball": 74,
    "jeans": 25
}

for query_name, query_number in query.items():
    os.mkdir(f"data/{query_name}")

    image_count = 0
    page_count = 1

    while image_count < query_number:
        url = f"https://unsplash.com/napi/search/photos?query={query_name}&per_page=20&page={page_count}"
        req = requests.get(url=url, headers=headers)
        data = json.loads(req.text)

        for item in data['results']:
            image_link = item["urls"]["full"]

            if "plus.unsplash" in image_link:
                continue

            h = httplib2.Http('.cache')
            response, content = h.request(image_link)
            image_file = open(f"data/{query_name}/{image_count}_{query_name}.jpg", "wb")
            image_file.write(content)
            image_file.close()

            image_count += 1
            if image_count >= query_number:
                break

        if image_count >= query_number:
            break

        page_count += 1