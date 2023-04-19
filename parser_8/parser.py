"""
Parser microservice
"""
import os
import json
import requests
import httplib2


def make_dirs(query, path):
    """
    Creates directories for output
    """
    if path[-1] != '/':
        path += '/'
    if not os.path.exists(path):
        os.makedirs(path)
    for query_name, _ in query.items():
        if not os.path.exists(f"{path}{query_name}/"):
            os.mkdir(f"{path}{query_name}/")


def download(url, output_name):
    """
    Downloads image from given url to output_name file
    """
    _, content = httplib2.Http('.cache').request(url)
    with open(output_name, 'wb') as out:
        out.write(content)


def search_on_openverse(name, count):
    """
    Searches name on https://openverse.org and parse image urls
    :return dict image urls
    """
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36",
        "Content-Type": "application/json",
        "Vary": "Accept"
    }

    page_counter = 1
    image_count = 0
    res = []
    while image_count < count:
        url = f"https://api.openverse.engineering/v1/images/?format=json&page={page_counter}&q={name}"
        try:
            req = response = requests.get(url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?

        data = json.loads(req.text)

        for item in data['results']:
            image_link = item['url']
            creator = item['creator']
            creator_url = item['creator_url']
            license_type = item['license']
            license_version = item['license_version']
            license_url = item['license_url']

            res.append({
                'creator': creator,
                'creator_url': creator_url,
                'license_type': license_type,
                'license_version': license_version,
                'license_url': license_url,
                'image_link': image_link
            })

            image_count += 1
            if image_count >= count:
                break
        page_counter += 1
    return res


def main():
    """
    Main function
    """

    query = {
        "waterfall": 100,
        "river": 100
    }

    path = "../imgs/"
    make_dirs(query, path)

    links_to_download = dict()
    for query_name, query_number in query.items():
        links_to_download[query_name] = search_on_openverse(query_name, query_number)

    for name, items in links_to_download.items():
        for index, item in enumerate(items):
            download(item['image_link'], f"{path}{name}/{index}.jpg")
        with open(f"{path}{name}/authority.json", "a", encoding="utf-8") as file:
            json.dump(links_to_download, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
