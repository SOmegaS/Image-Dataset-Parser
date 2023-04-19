import requests
from bs4 import BeautifulSoup as bs


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


def search_images_by_links(list_of_links, count):
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
