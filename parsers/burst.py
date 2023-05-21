import csv
from math import floor

import requests
from bs4 import BeautifulSoup

from parsers.base_parser import Parser


class Burst(Parser):
    def search(self, name, count, number_of_parser, start=0):
        """
        Searches name on unsplash.com and parse image urls
        :return dict image urls
        """
        page_counter = floor(start / 200) + 1
        image_count = start
        res = []
        with open(self.path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'a') as file:
            writer = csv.writer(file)
            if image_count == 0:
                writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            while image_count < count:
                url = f"https://burst.shopify.com/photos/search?" \
                      f"q={name}&" \
                      f"page={page_counter}"
                try:
                    req = requests.get(url=url, timeout=1000)
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
