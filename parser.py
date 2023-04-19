import os
import sys
import httplib2
import requests
from parsers import unsplash
from parsers import openverse
from parsers import vecteezy
from parsers import publicdomain
from parsers import unsplash
from parsers import wikimedia
from parsers import google

amount_const = 7
sz = [1 / 7] * 7
path = "./images"
func = [search_on_unsplash, parse_page, search_on_wikimedia, search_on_burst, search_on_vecteezy, search_on_google, search_on_openverse]


def make_dirs(query, dirs_path):  # copypaste from Parser1
    if dirs_path[-1] != '/':
        dirs_path += '/'
    if not os.path.exists(dirs_path):
        os.makedirs(dirs_path)
    for query_name, _ in query.items():
        if not os.path.exists(f"{dirs_path}{query_name}/"):
            os.mkdir(f"{dirs_path}{query_name}/")


def download(url, output_name):  # copypaste from Parser1
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


def parse(request, size, links):
    for i in range(amount_const):
        for index, link in enumerate(func[i](request, size * sz[i])):  # get links array
            if func[i] == search_on_vecteezy:
                download_without_cash(link, f"{path}{request}/{index}.jpg")
            download(link, f"{path}{request}/{index}.jpg")  # download for each parser


def main(args=None):
    if args is None:
        args = sys.argv
    query = {}
    count = args[-1]
    for cls in args[:-1]:
        query[cls] = count
    dirs_path = path
    make_dirs(query, dirs_path)  # make directories first for all parsers output
    links = {}
    for (request, size) in query.items():
        parse(request, size, links)


if __name__ == "__main__":
    main()
