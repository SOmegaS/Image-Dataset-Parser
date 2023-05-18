import csv
import json
from math import floor

import requests

from parsers.base_parser import Parser


class Wikimedia(Parser):
    def search(self, name, count, number_of_parser, start=0):
        """
        Searches name on https://commons.wikimedia.org and parse image urls
        :return dict image urls
        """
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.998 Yowser/2.5 Safari/537.36"
        }

        page_counter = floor(start / 40) + 1
        image_count = start
        res = []
        with open(self.path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            if image_count == 0:
                writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            while image_count < count:
                url = f"https://commons.m.wikimedia.org/w/api.php?action=query&format=json&uselang=en&generator=search&gsrsearch=filetype%3Abitmap%7Cdrawing%20-fileres%3A0%20{name}&gsrlimit=40&gsroffset={page_counter * 40}&gsrinfo=totalhits%7Csuggestion&gsrprop=size%7Cwordcount%7Ctimestamp%7Csnippet&prop=info%7Cimageinfo%7Centityterms&inprop=url&gsrnamespace=6&iiprop=url%7Csize%7Cmime&iiurlheight=180&wbetterms=label"
                try:
                    req = requests.get(url=url, headers=headers, timeout=1000)
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
