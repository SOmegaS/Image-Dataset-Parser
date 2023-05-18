import csv
from math import floor

import requests
import json

from parsers.base_parser import Parser


class Openverse(Parser):
    def search(self, name, count, number_of_parser, start=0):
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

        page_counter = floor(start / 20) + 1
        image_count = start
        res = []
        with open(self.path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'a') as file:
            writer = csv.writer(file)
            if image_count == 0:
                writer.writerow(
                    ['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version',
                     'license_url'])
            while image_count < count:
                url = f"https://api.openverse.engineering/v1/images/?format=json&page={page_counter}&q={name}"
                try:
                    req = requests.get(url, headers=headers, timeout=1000)
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
