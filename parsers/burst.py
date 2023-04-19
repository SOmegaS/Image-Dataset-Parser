import requests
from bs4 import BeautifulSoup


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
                # print(img["src"][start:end])
                res.append(img["src"][start:end] + "?width=1024")
                image_count += 1
                if image_count >= count:
                    break
            except KeyError:
                pass
        page_counter += 1
    return res
