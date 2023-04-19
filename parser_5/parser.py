"""
Parser microservice
"""
import os
import requests
import httplib2
from bs4 import BeautifulSoup


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


def search_on_burst(name, count):
    """
    Searches name on unsplash.com and parse image urls
    :return dict image urls
    """
    page_counter = 1
    image_count = 0
    res = []
    while image_count < count:
        url = f"https://burst.shopify.com/photos/search?" \
              f"q={name}&" \
              f"page={page_counter}"
        try:
            req = requests.get(url=url, timeout=5)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?

        soup = BeautifulSoup(req.text, "html.parser")
        imgs = soup.find_all("img")
        res = []
        for img in imgs:
            try:
                start = img["src"].rfind("https://")
                end = img["src"].rfind("?width=")
                print(img["src"][start:end])
                res.append(img["src"][start:end] + "?width=1024")
                image_count += 1
                if image_count >= count:
                    break
            except KeyError:
                pass
        page_counter += 1
    return res


def main():
    """
    Main function
    """

    query = {
        "mouse": 10,
        "computer": 10
    }

    path = "../imgs/"
    make_dirs(query, path)

    links_to_download = dict()
    for query_name, query_number in query.items():
        links_to_download[query_name] = search_on_burst(query_name, query_number)

    for name, links in links_to_download.items():
        for index, link in enumerate(links):
            download(link, f"{path}{name}/{index}.jpg")


if __name__ == '__main__':
    main()
