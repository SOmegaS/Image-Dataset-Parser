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


def search_on_wikimedia(name, count):
    """
    Searches name on https://commons.wikimedia.org and parse image urls
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
        url = f"https://commons.m.wikimedia.org/w/api.php?action=query&format=json&uselang=en&generator=search&gsrsearch=filetype%3Abitmap%7Cdrawing%20-fileres%3A0%20{name}&gsrlimit=40&gsroffset={page_counter * 40}&gsrinfo=totalhits%7Csuggestion&gsrprop=size%7Cwordcount%7Ctimestamp%7Csnippet&prop=info%7Cimageinfo%7Centityterms&inprop=url&gsrnamespace=6&iiprop=url%7Csize%7Cmime&iiurlheight=180&wbetterms=label"
        try:
            req = requests.get(url=url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout:
            continue  # What to do?
        data = json.loads(req.text)

        for item in data['query']['pages']:
            image_link = data['query']['pages'][item]['imageinfo'][0]['url']

            res.append(image_link)

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
        "train": 100,
    }

    path = "../imgs/"
    make_dirs(query, path)

    links_to_download = dict()
    for query_name, query_number in query.items():
        links_to_download[query_name] = search_on_wikimedia(query_name, query_number)

    for name, links in links_to_download.items():
        for index, link in enumerate(links):
            download(link, f"{path}{name}/{index}.jpg")


if __name__ == '__main__':
    main()
