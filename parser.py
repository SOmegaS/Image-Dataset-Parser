"""
Parser microservice
"""
import os
import time
import httplib2
import requests
from bs4 import BeautifulSoup


def download(url, output_name):
    """
    Downloads image from given url to output_name file
    """
    _, content = httplib2.Http('.cache').request(url)
    with open(output_name, 'wb') as out:
        out.write(content)


def search_on_unsplash(name):
    """
    Searches name on unsplash.com and parse image urls
    :return list image urls
    """
    url = "https://unsplash.com/s/photos/" + name
    soup = BeautifulSoup(requests.get(url, timeout=0.5).text, "html.parser")
    imgs = soup.find_all("img")
    res = []
    for img in imgs:
        try:
            start = img["srcset"].rfind("https://")
            end = img["srcset"].rfind(" ")
            res.append(img["srcset"][start:end])
        except KeyError:
            pass
    return res


def main():
    """
    Main function
    """
    start = time.time()
    urls = search_on_unsplash('dog')
    if not os.path.exists("imgs/"):
        os.makedirs("imgs/")
    for key, val in enumerate(urls):
        download(val, "imgs/" + str(key) + ".jpg")
    print(time.time() - start)


if __name__ == '__main__':
    main()
