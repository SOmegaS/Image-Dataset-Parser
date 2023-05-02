import json
import os
import sys
import csv
import httplib2
import requests
from bs4 import BeautifulSoup
#from google_images_search import GoogleImagesSearch

path = "images/"
path_for_save = "save/"

class Parser:

    @staticmethod
    def make_dirs(query, dirs_path, save_path, parser_count):
        if dirs_path[-1] != '/':
            dirs_path += '/'
        if save_path[-1] != '/':
            save_path += '/'
        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for query_name, _ in query.items():
            if not os.path.exists(f"{dirs_path}{query_name}/"):
                os.mkdir(f"{dirs_path}{query_name}/")
        for i in range(1, parser_count + 1):
            os.mkdir(f"{save_path}{i}")
            for query_name, _ in query.items():
                if not os.path.exists(f"{save_path}{str(i)}/{query_name}/"):
                    os.mkdir(f"{save_path}{i}/{query_name}")

    def download(self, url, output_name):
        _, content = httplib2.Http('.cache').request(url)
        with open(output_name, 'wb') as out:
            out.write(content)

    def parse(self, query, perc, number_of_parser):
        links_to_download = dict()
        for query_name, query_number in query.items():
            num = round(query_number * perc)
            links_to_download[query_name] = self.search(query_name, num, number_of_parser)
        for name, links in links_to_download.items():
            for index, link in enumerate(links):  # get links array
                self.download(link,
                              f"{path}{name}/{index + 1}_{self.__class__.__name__}.jpg")  # download

    @staticmethod
    def links_from_file(last_id, path_to_file):
        """
        get list of links from file from last_id
        """
        links = []
        with open(path_to_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['id']) > last_id:
                    links.append(row['link'])
        return links

    def search(self, name, count, number_of_parser):
        pass

    def search_images_by_links(self, list_of_links, name, count, number_of_parser):
        pass


class Burst(Parser):

    def search(self, name, count, number_of_parser):
        """
        Searches name on unsplash.com and parse image urls
        :return dict image urls
        """
        page_counter = 1
        image_count = 0
        res = []
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
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
                for img in imgs:
                    try:
                        start = img["src"].rfind("https://")
                        end = img["src"].rfind("?width=")
                        # print(img["src"][start:end])
                        res.append(img["src"][start:end] + "?width=1024")
                        image_count += 1
                        writer.writerow([image_count, res[-1], "-", "-", "-", "-", "-"])
                        if image_count >= count:
                            break
                    except KeyError:
                        pass
                page_counter += 1
        return res


class Google(Parser):
    def search(self, name, count, number_of_parser):
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
        result = []
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            image_count = 0
            for image in gis.results():
                result.append(image)
                image_count += 1
                writer.writerow([image_count, result[-1], "-", "-", "-", "-", "-"])
        return result


class Openverse(Parser):

    def search(self, name, count, number_of_parser):
        """
        Searches name on https://openverse.org and parse image urls
        :return dict image urls
        """
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36",
            "Content-Type": "application/json",
            "Vary": "Accept"
        }

        page_counter = 1
        image_count = 0
        res = []
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            while image_count < count:
                url = f"https://api.openverse.engineering/v1/images/?format=json&page={page_counter}&q={name}"
                try:
                    req = response = requests.get(url, headers=headers, timeout=1)
                except requests.exceptions.ReadTimeout:
                    continue  # What to do?

                data = json.loads(req.text)

                for item in data['results']:
                    image_link = item['url']
                    creator = item['creator']
                    creator_url = item['creator_url']
                    license_type = item['license']
                    license_version = item['license_version']
                    license_url = item['license_url']
                    res.append(image_link)
                    image_count += 1
                    writer.writerow([image_count, res[-1], creator, creator_url, license_type,
                                     license_version, license_url])

                    if image_count >= count:
                        break
                page_counter += 1
        return res


# class PublicDomain(Parser):
#
#     def __init__(self):
#         self.image_count = 0
#
#     def parse_page(self, current_url, query_name, query_number, path, idx):
#
#         headers = {
#             "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
#         }
#
#         main_page = requests.get(current_url, headers=headers)
#         main_page_src = main_page.text
#
#         main_page_soup = BeautifulSoup(main_page_src, "lxml")
#
#         images_containers = main_page_soup.find_all("div", class_="thumbnail blog-thumb")
#
#         for container in images_containers:
#             if container is None:
#                 exit()
#
#             image_source = container.find("a").get("href")
#
#             image_page = requests.get(image_source, headers=headers)
#             image_page_src = image_page.text
#
#             image_page_soup = BeautifulSoup(image_page_src, "lxml")
#
#             image_href = image_page_soup.find("div", class_="wp-caption aligncenter").find("a").get("href")
#
#             h = httplib2.Http('.cache')
#             response, content = h.request(image_href)
#
#             image_file = open(f"{path}{query_name}/{self.image_count}_parser{idx}.jpg", "wb")
#             image_file.write(content)
#             image_file.close()
#
#             self.image_count += 1
#             if self.image_count >= query_number:
#                 break
#
#     def search(self, cur_query_name, cur_query_number, path, idx, number):
#         page_count = 1
#         while self.image_count < cur_query_number:
#             url = f"https://www.photos-public-domain.com/page/{page_count}/?s={cur_query_name}"
#             cur_query_number = number
#             self.parse_page(url, cur_query_name, cur_query_number, path, idx)
#             page_count += 1


class Unsplash(Parser):

    def search(self, name, count, number_of_parser):
        """
        Searches name on unsplash.com and parse image urls
        :return dict image urls
        """
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
        }

        page_counter = 1
        image_count = 0
        res = []
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            while image_count < count:
                url = f"https://unsplash.com/napi/search/photos?" \
                      f"query={name}&" \
                      f"per_page=20&page={page_counter}"
                try:
                    req = requests.get(url=url, headers=headers, timeout=1)
                except requests.exceptions.ReadTimeout:
                    continue  # What to do?
                data = json.loads(req.text)

                for item in data['results']:
                    image_link = item["urls"]["full"]

                    if "plus.unsplash" in image_link:
                        continue

                    res.append(image_link)
                    image_count += 1
                    writer.writerow([image_count, res[-1], "-", "-", "-", "-", "-"])

                    if image_count >= count:
                        break
                page_counter += 1
        return res


class Vecteezy(Parser):

    def download(self, url, output_name):
        """
            Downloads image from given url to output_name file for vecteezy
            """
        resource = requests.get(url)
        out = open(output_name, 'wb')
        out.write(resource.content)
        out.close()

    def search(self, name, count, number_of_parser):
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
            soup = BeautifulSoup(req.content, 'html.parser')
            links = soup.findAll('a', {'class': 'ez-resource-thumb__link'})
            links = links[1::2]
            for item in links:
                link = item['href']
                res.append(link)
                image_count += 1
                if image_count >= count:
                    break
            page_counter += 1
        return self.search_images_by_links(res, name, count, number_of_parser)

    def search_images_by_links(self, list_of_links, name, count, number_of_parser):
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
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            while image_count < count:
                url = list_of_links[image_count]
                try:
                    req = requests.get(url=url, headers=headers, timeout=1)
                except requests.exceptions.ReadTimeout:
                    continue  # What to do?
                soup = BeautifulSoup(req.content, 'html.parser')
                links = soup.findAll('img', {'class': 'ez-resource-show__preview__image'})
                for item in links:
                    link = item['src']
                    res.append(link)
                    image_count += 1
                    writer.writerow([image_count, res[-1], "-", "-", "-", "-", "-"])
                    if image_count >= count:
                        break
                page_counter += 1
        return res


class Wikimedia(Parser):
    def search(self, name, count, number_of_parser):
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
        with open(path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
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
                    writer.writerow([image_count, res[-1], "-", "-", "-", "-", "-"])

                    if image_count >= count:
                        break
                page_counter += 1
        return res


def main():
    parser = Parser()
    parsers = [Vecteezy(), Burst(), Openverse(), Unsplash(), Wikimedia()]
    amount_const = len(parsers)
    perc = 1 / amount_const
    # sz = [perc] * (amount_const - 1)
    query = {  # testing query
        "train": 100
    }
    parser.make_dirs(query, path, path_for_save, amount_const)
    for i in range(0, amount_const):
        parsers[i].parse(query, perc, i + 1)


if __name__ == "__main__":
    main()
