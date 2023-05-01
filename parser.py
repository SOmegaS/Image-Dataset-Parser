import json
import os
import sys
import httplib2
import requests
from bs4 import BeautifulSoup
from google_images_search import GoogleImagesSearch

path = "../images/"


class Parser:

    @staticmethod
    def make_dirs(query, dirs_path):
        if dirs_path[-1] != '/':
            dirs_path += '/'
        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        for query_name, _ in query.items():
            if not os.path.exists(f"{dirs_path}{query_name}/"):
                os.mkdir(f"{dirs_path}{query_name}/")

    def download(self, url, output_name):
        _, content = httplib2.Http('.cache').request(url)
        with open(output_name, 'wb') as out:
            out.write(content)

    def parse(self, query, perc):
        links_to_download = dict()
        for query_name, query_number in query.items():
            num = round(query_number * perc)
            links_to_download[query_name] = self.search(query_name, num)
        for name, links in links_to_download.items():
            for index, link in enumerate(links):  # get links array
                if self.__class__.__name__ == "Openverse":  # this should be done for each parser at the end (licences)
                    link = link['image_link']
                self.download(link,
                              f"{path}{name}/{index + 1}_{self.__class__.__name__}.jpg")  # download
            if self.__class__.__name__ == "Openverse":
                with open(f"{path}{name}/authority.json", "a", encoding="utf-8") as file:
                    json.dump(links_to_download, file, indent=4, ensure_ascii=False)

    def search(self, name, count):
        pass

    def search_images_by_links(self, list_of_links, count):
        pass


class Burst(Parser):

    def search(self, name, count):
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


class Google(Parser):

    def search(self, name, count):
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


class Openverse(Parser):

    def search(self, name, count):
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

                res.append({
                    'creator': creator,
                    'creator_url': creator_url,
                    'license_type': license_type,
                    'license_version': license_version,
                    'license_url': license_url,
                    'image_link': image_link
                })

                image_count += 1
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

    def search(self, name, count):
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

    def search(self, name, count):
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
        return self.search_images_by_links(res, count)

    def search_images_by_links(self, list_of_links, count):
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
            soup = BeautifulSoup(req.content, 'html.parser')
            links = soup.findAll('img', {'class': 'ez-resource-show__preview__image'})
            for item in links:
                link = item['src']
                res.append(link)
                image_count += 1
                if image_count >= count:
                    break
            page_counter += 1
        return res


class Wikimedia(Parser):
    def search(self, name, count):
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
    parser = Parser()
    parsers = [Vecteezy(), Burst(), Openverse(), Unsplash(), Wikimedia()]
    amount_const = len(parsers)
    perc = 1 / amount_const
    # sz = [perc] * (amount_const - 1)
    query = {  # testing query
        "train": 100
    }
    parser.make_dirs(query, path)
    for prs in parsers:
        prs.parse(query, perc)


if __name__ == "__main__":
    main()
