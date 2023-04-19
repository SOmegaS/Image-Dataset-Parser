"""
Parser microservice
"""
import os
import httplib2
from google_images_search import GoogleImagesSearch


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


def search_on_google(name, count):
    """
    Searches name on google.com and parse image urls
    :return dict image urls
    """
    # your keys here
    gis = GoogleImagesSearch('api_key', 'search_system_id')
    _search_params = {
        'q': name,
        'num': count,
        'fileType': 'jpg|png',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        # 'safe': 'active|high|medium|off|safeUndefined',  ##
        # 'imgType': 'clipart|face|lineart|stock|photo|animated|imgTypeUndefined',  ##
        # 'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined',  ##
        # 'imgDominantColor':
        # 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined', ##
        # 'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined'  ##
    }
    gis.search(search_params=_search_params)
    return [image.url for image in gis.results()]


def main():
    """
    Main function
    """

    query = {
        "mouse": 50,
        "computer": 50,
    }

    path = "../imgs/"
    make_dirs(query, path)
    links_to_download = dict()
    for query_name, query_number in query.items():
        links_to_download[query_name] = search_on_google(query_name, query_number)
        print("ok")
    print("search completed\n")
    for name, links in links_to_download.items():
        for index, link in enumerate(links):
            download(link, f"{path}{name}/{index}.jpg")
            print(end='+')
        print("\nok")


if __name__ == '__main__':
    main()
