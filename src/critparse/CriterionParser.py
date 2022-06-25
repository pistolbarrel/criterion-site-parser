import requests
from bs4 import BeautifulSoup
import argparse
from critparse import CriterionParser, CriterionMovieParse, TextOut




class CriterionParser:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html5lib')
        self.url_type = CriterionParser.determine_url_type(self.soup)
        self.series_name = ''
        self.all_movie_parsed_data = []
        self.time = None
        self.extracted_episode_info = None
        self.description = None

    def gather_all_info(self):
        if self.url_type == 'movie':
            self.__gather_movie_list_info([['', self.url]])
        elif self.url_type == 'collection':
            self.series_name, self.extracted_episode_info = CriterionParser.get_collection_info(self.soup)
            self.__gather_movie_list_info(self.extracted_episode_info)
        elif self.url_type == 'edition':
            self.series_name, self.extracted_episode_info = CriterionParser.get_edition_info(self.soup)
            self.__gather_movie_list_info(self.extracted_episode_info)
        else:
            self.series_name, self.description, self.extracted_episode_info = CriterionParser.get_series_info(self.soup)
            self.__gather_movie_list_info(self.extracted_episode_info)

    def __gather_movie_list_info(self, movies_list):
        for movie in movies_list:
            time, url = movie[0], movie[1]
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            url_type = CriterionParser.determine_url_type(soup)
            if url_type == 'collection':
                time, url = CriterionParser.extract_collection_title_feature(soup)[0]
                if time == '0:00':
                    continue
            movie_parser = CriterionMovieParse.MovieParse(url, time)
            self.all_movie_parsed_data.append(movie_parser.get_parsed_info())

    def collect_information_for_api(self):
        if self.url_type == 'movie':
            print('Examined ' + self.url)
            CriterionParser.call_api([['', self.url]], self.series_name)
        elif self.url_type == 'collection':
            self.series_name, self.extracted_episode_info = CriterionParser.get_collection_info(self.soup)
            print('Examined ' + self.url)
            CriterionParser.call_api(self.extracted_episode_info, self.series_name)
        elif self.url_type == 'edition':
            self.series_name, self.extracted_episode_info = CriterionParser.get_edition_info(self.soup)
            print('Examined ' + self.url)
            CriterionParser.call_api(self.extracted_episode_info, self.series_name)
        else:
            self.series_name, self.description, self.extracted_episode_info = CriterionParser.get_series_info(self.soup)
            print('Examined ' + self.url)
            print('+' * 54)
            print(self.series_name)
            print(self.description)
            print('+' * 54)
            print()
            print()
            # self.print_movies_list(self.extracted_episode_info)
            CriterionParser.call_api(self.extracted_episode_info, self.series_name)

    @staticmethod
    def get_series_info(soup):
        series_name, description = CriterionParser.extract_series_name_and_description(soup)
        series_name = "Criterion:" + series_name
        series = CriterionParser.extract_episode_time_and_url(soup)
        next_url = CriterionParser.extract_next_url(soup)
        while next_url:
            r = requests.get(next_url)
            soup = BeautifulSoup(r.content, 'html5lib')
            next_url = CriterionParser.extract_next_url(soup)
            series += CriterionParser.extract_episode_time_and_url(soup)
        return series_name, description, series

    @staticmethod
    def call_api(movies_list, series_name):
        episode = 0
        for movie in movies_list:
            episode += 1
            time, url, title = movie
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            url_type = CriterionParser.determine_url_type(soup)
            if url_type == 'collection':
                time, url = CriterionParser.extract_collection_title_feature(soup)[0]
            movie_parser = CriterionMovieParse.MovieParse(url)
            movie_parser.addViaApi(time, series_name)

    @staticmethod
    def extract_next_url(soup):
        ret_str = None
        table = soup.find('div', attrs={'class': 'row loadmore'})
        if table:
            for item in table.findAll('a', attrs={'class': 'js-load-more-link'}):
                ret_str = "https://www.criterionchannel.com" + item['href']
        return ret_str

    @staticmethod
    def determine_url_type(soup):
        match_star = 'Starring '
        match_edition = 'Criterion Collection Edition '
        url_type = None
        one, two = CriterionParser.url_type_helper(soup)
        if one == 'NoName' and two == 'NoDescription':
            url_type = 'movie'
        elif url_type is None and two[:len(match_star)] == match_star:
            url_type = 'collection'
        elif url_type is None and one[:len(match_edition)] == match_edition:
            url_type = 'edition'
        elif url_type is None:
            url_type = 'series'
        return url_type

    @staticmethod
    def extract_series_name_and_description(soup):
        match = 'Criterion Collection Edition '
        ret_str = ['NoName', 'NoAddition', 'NoDescription']
        table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
        if table:
            ret_str = []
            for string in table.stripped_strings:
                ret_str.append(string)
            if ret_str[1][:len(match)] == match:
                ret_str[0] = ret_str[1]
        return ret_str[0], ret_str[2]

    @staticmethod
    def url_type_helper(soup):
        series_name, description = CriterionParser.extract_series_name_and_description(soup)
        return series_name, description

    @staticmethod
    def extract_collection_title_feature(soup):
        ret = []
        table = soup.find('li', attrs={'class': 'js-collection-item'})
        if table:
            for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
                movie = [item.a.text.strip(), item.a['href']]
                ret.append(movie)
        if len(ret) == 0:
            empty = ['0:00', 'NoLinkToFeature']
            ret.append(empty)
        return ret

    @staticmethod
    def extract_episode_time_and_url(soup):
        ret = []
        table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
        if table:
            for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
                movie = [item.a.text.strip(), item.a['href'], item.img['alt']]
                ret.append(movie)
        return ret

    @staticmethod
    def get_collection_info(soup):
        series_name, not_used = CriterionParser.extract_series_name_and_description(soup)
        series_name = "Collection:" + series_name
        series = CriterionParser.extract_collection_title_feature(soup)
        series += CriterionParser.extract_episode_time_and_url(soup)
        return series_name, series

    @staticmethod
    def get_edition_info(soup):
        series_name, not_used = CriterionParser.extract_series_name_and_description(soup)
        series = CriterionParser.extract_collection_title_feature(soup)
        series += CriterionParser.extract_episode_time_and_url(soup)
        return series_name, series


def main():
    args = process_args()
    if args.url:
        parser = CriterionParser(args.url)
        if args.api:
            parser.collect_information_for_api()
        else:
            parser.gather_all_info()
            TextOut.movie_info_to_text()


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-a", "--api", help="Add movie via REST api", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
