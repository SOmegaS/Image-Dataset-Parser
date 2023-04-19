import json
import os
import sys
import httplib2
import requests
from parsers.burst import search_on_burst
from parsers.google import search_on_google
from parsers.openverse import search_on_openverse
from parsers.publicdomain import search_on_publicdomain
from parsers.unsplash import search_on_unsplash
from parsers.vecteezy import search_on_vecteezy, search_images_by_links
from parsers.wikimedia import search_on_wikimedia

path = "../images/"
func = [search_on_unsplash, search_on_openverse, search_on_wikimedia, search_on_publicdomain, search_on_burst]
amount_const = len(func)
part = 1 / amount_const
sz = [part] * (amount_const - 1)


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


def parse(query):
    for i in range(amount_const):
        links_to_download = dict()
        links_to_images = dict()
        done = 0
        for query_name, query_number in query.items():
            if i + 1 == amount_const:
                # num = query_number - done
                num = round(query_number * sz[i - 1])
                done = query_number
            else:
                num = round(query_number * sz[i])
                done += num
            if func[i] == search_on_publicdomain:
                search_on_publicdomain(query_name, query_number, path, i, num)
                continue
            if func[i] == search_on_vecteezy:
                links_to_images[query_name] = search_on_vecteezy(query_name, num)
                links_to_download[query_name] = search_images_by_links(links_to_images[query_name],
                                                                       num)
            else:
                links_to_download[query_name] = func[i](query_name, num)
        for name, links in links_to_download.items():
            for index, link in enumerate(links):  # get links array
                if func[i] == search_on_vecteezy:
                    download_without_cash(link, f"{path}{name}/{index}_parser{i}.jpg")
                if func[i] == search_on_openverse:
                    link = link['image_link']
                download(link, f"{path}{name}/{index}_parser{i}.jpg")  # download for each parser
            if func[i] == search_on_openverse:
                with open(f"{path}{name}/authority.json", "a", encoding="utf-8") as file:
                    json.dump(links_to_download, file, indent=4, ensure_ascii=False)


def main(args=None):
    # if args is None:
    #     args = sys.argv
    # query = {}
    # count = args[-1]
    # for cls in args[:-1]:
    #     query[cls] = count
    query = {
        "cat": 20,
        "dog": 20
    }
    dirs_path = path
    make_dirs(query, dirs_path)  # make directories first for all parsers output
    parse(query)


if __name__ == "__main__":
    main()
