import csv
from math import floor

import requests
from bs4 import BeautifulSoup

from parsers.base_parser import Parser


class Vecteezy(Parser):

    def download(self, url, output_name):
        """
            Downloads image from given url to output_name file for vecteezy
            """
        resource = requests.get(url)
        out = open(output_name, 'wb')
        out.write(resource.content)
        out.close()

    def search(self, name, count, number_of_parser, start=0):
        """
        Searches name on https://vecteezy.com and parse image urls
        :return dict image urls
        """
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36"
        }

        page_counter = floor(start / 100) + 1  # 100 images per request
        image_count = start
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
        return self.search_images_by_links(res, name, count, number_of_parser, start)

    def search_images_by_links(self, list_of_links, name, count, number_of_parser, start):
        """
            Searches name on https://vecteezy.com and parse image urls
            :return dict image urls
        """
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36"
        }

        image_count = start
        res = []
        with open(self.path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'a') as file:
            writer = csv.writer(file)
            if image_count == 0:
                writer.writerow(
                    ['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version',
                     'license_url'])
            while image_count < count:
                url = 'https://vecteezy.com' + list_of_links[image_count - start]
                tries = 1
                try:
                    req = requests.get(url=url, headers=headers, timeout=1000)
                except Exception:
                    if tries >= 5:
                        break
                    tries += 1
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
        return res
