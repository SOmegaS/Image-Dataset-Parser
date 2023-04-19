"""
Parser microservice
"""
import os
import requests
import httplib2
from bs4 import BeautifulSoup as bs


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


def download_without_cash(url, output_name):
    """
        Downloads image from given url to output_name file for vecteezy
        """
    resource = requests.get(url)
    out = open(output_name, 'wb')
    out.write(resource.content)
    out.close()


def search_on_vecteezy(name, count):
    """
    Searches name on https://vecteezy.com and parse image urls
    :return dict image urls
    """
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36"
    }

    page_counter = 0
    image_count = 0
    res = []
    while image_count < count:
        url = f"https://vecteezy.com/free-photos/{name}?license-free=true&page={page_counter}"
        try:
            req = requests.get(url=url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?
        soup = bs(req.content, 'html.parser')
        links = soup.findAll('a', {'class': 'ez-resource-thumb__link'})
        links = links[1::2]
        for item in links:
            link = 'https://vecteezy.com' + item['href']
            res.append(link)
            image_count += 1
            if image_count >= count:
                break
        page_counter += 1
    return res


def search_images_by_links(list_of_links, count) :
    """
        Searches name on https://vecteezy.com and parse image urls
        :return dict image urls
    """
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36"
    }

    page_counter = 0
    image_count = 0
    res = []
    while image_count < count:
        url = list_of_links[image_count]
        try:
            req = requests.get(url=url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?
        soup = bs(req.content, 'html.parser')
        links = soup.findAll('img', {'class': 'ez-resource-show__preview__image'})
        for item in links:
            link = item['src']
            res.append(link)
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
        "dog": 10,
    }

    path = "../imgs/"
    make_dirs(query, path)

    links_to_download = dict()
    links_to_images = dict()
    for query_name, query_number in query.items():
        links_to_images[query_name] = search_on_vecteezy(query_name, query_number)
        links_to_download[query_name] = search_images_by_links(links_to_images[query_name], query_number)

    for name, links in links_to_download.items():
        for index, link in enumerate(links):
            download_without_cash(link, f"{path}{name}/{index}.jpg")


if __name__ == '__main__':
    main()