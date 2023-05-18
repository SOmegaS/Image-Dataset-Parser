import csv
import os
import httplib2


class Parser:
    def __init__(self, path, path_for_save):
        self.path = path
        self.path_for_save = path_for_save

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
            if not os.path.exists(f"{save_path}{i}"):
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
            links_to_download[query_name] = []
            if os.path.exists(f"{self.path_for_save}{number_of_parser}/{query_name}/db.csv"):
                links_to_download[query_name] = self.links_from_file(0,
                                                                     f"{self.path_for_save}{number_of_parser}/{query_name}/db.csv")[
                                                :num]
            if len(links_to_download[query_name]) < num:
                start = len(links_to_download[query_name])
                links_to_download[query_name] = links_to_download[query_name] + self.search(
                    query_name, num,
                    number_of_parser,
                    start)
        for name, links in links_to_download.items():
            for index, link in enumerate(links):  # get links array
                if not os.path.exists(f"{self.path}{name}/{index + 1}_{self.__class__.__name__}.jpg"):
                    self.download(link,
                              f"{self.path}{name}/{index + 1}_{self.__class__.__name__}.jpg")  # download

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

    def search(self, name, count, number_of_parser, start) -> list:
        pass

    def search_images_by_links(self, list_of_links, name, count, number_of_parser, start):
        pass
