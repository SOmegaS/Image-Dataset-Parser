import requests
import httplib2
from bs4 import BeautifulSoup

image_count = 0
def parse_page(current_url, query_name, query_number, path, idx):
    global image_count

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
    }

    main_page = requests.get(current_url, headers=headers)
    main_page_src = main_page.text

    main_page_soup = BeautifulSoup(main_page_src, "lxml")

    images_containers = main_page_soup.find_all("div", class_="thumbnail blog-thumb")

    for container in images_containers:
        if container is None:
            exit()

        image_source = container.find("a").get("href")

        image_page = requests.get(image_source, headers=headers)
        image_page_src = image_page.text

        image_page_soup = BeautifulSoup(image_page_src, "lxml")

        image_href = image_page_soup.find("div", class_="wp-caption aligncenter").find("a").get("href")

        h = httplib2.Http('.cache')
        response, content = h.request(image_href)

        image_file = open(f"{path}{query_name}/{image_count}_parser{idx}.jpg", "wb")
        image_file.write(content)
        image_file.close()

        image_count += 1
        if image_count >= query_number:
            break


def search_on_publicdomain(cur_query_name, cur_query_number, path, idx, number):
    page_count = 1
    while image_count < cur_query_number:
        url = f"https://www.photos-public-domain.com/page/{page_count}/?s={cur_query_name}"
        cur_query_number = number
        parse_page(url, cur_query_name, cur_query_number, path, idx)
        page_count += 1
