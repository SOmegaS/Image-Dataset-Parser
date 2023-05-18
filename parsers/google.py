import csv
from google_images_search import GoogleImagesSearch

from parsers.base_parser import Parser


class Google(Parser):

    def __init__(self, path, path_for_save, api_key, search_system_id):
        super().__init__(path, path_for_save)
        self.api_key = api_key
        self.search_system_id = search_system_id

    def search(self, name, count, number_of_parser, start):
        """
        Searches name on google.com and parse image urls
        :return dict image urls
        """
        # your keys here
        gis = GoogleImagesSearch(f'{self.api_key}', f'{self.search_system_id}')
        _search_params = {
            'q': name,
            'num': count,
            'fileType': 'jpg|png',
            'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        }
        gis.search(search_params=_search_params)
        result = []
        with open(self.path_for_save + str(number_of_parser) + "/" + name + "/db.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'creator', 'creator_url', 'license_type', 'license_version', 'license_url'])
            image_count = 0
            for image in gis.results():
                result.append(image)
                image_count += 1
                writer.writerow([image_count, result[-1], "-", "-", "-", "-", "-"])
        return result
