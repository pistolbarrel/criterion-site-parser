import json

import requests
from bs4 import BeautifulSoup, Tag
import argparse


def valueIfDefinedOrNONE(value):
    return value if value else "NONE"


def extract_director(item):
    return extract_from_dict(item, 'director', 'name')


def extract_country(item):
    return extract_from_dict(item, 'countryOfOrigin', 'name')


def extract_stars(item):
    ext_stars = extract_from_dict(item, 'actor', 'name')
    if not ext_stars:
        ext_stars = ''
    return ext_stars


def extract_from_dict(item, key, value):
    data_dict = json.loads(item.string)
    outStr = ''
    if key in data_dict:
        for item in data_dict[key]:
            outStr = outStr + item[value] + '; '

    if outStr != '':
        return outStr[:-2]
    else:
        return None


def extract_title_year_length(item):
    data_dict = json.loads(item.string)
    return data_dict['name'], data_dict['datePublished'], data_dict['duration']


def sanitize_year(year):
    if year != '':
        year = year[0:4]
    return year


def parse_length(length):

    if length == '':
        return ''
    hours = minutes = seconds = '00'

    index = length.find('hr')
    if index != -1:
        hours = length[:index]
        hours = hours.strip()
        length = length[index + 2:]
    index = length.find('min')
    if index != -1:
        minutes = length[:index]
        minutes = "0" + minutes.strip()
        minutes = minutes[-2:]
        length = length[index + 3:]
    index = length.find('S')
    if index != -1:
        seconds = length[:index]
        seconds = "0" + seconds
        seconds = seconds[-2:]

    if '00' not in hours:
        return hours + ':' + minutes + ':' + seconds
    else:
        return minutes + ':' + seconds


def sanitize_title(title):
    if title != '':
        if title[0:4] == "The ":
            title = title[4:] + ", " + title[0:3]
        if title[0:2] == "A ":
            title = title[2:] + ", " + title[0:1]
    title = title.replace(";", "_")
    return title

class SupplementParse:
    def __init__(self, url, time_supplied=None):
        self.url = url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        self.director = self.title = self.year = self.length = self.country = self.stars = self.descr = ''
        self.collect_movie_data(soup)


        self.title = sanitize_title(self.title)
        self.year = sanitize_year(self.year)
        self.titleWithYear = self.title + ' (' + self.year + ')'

    def collect_movie_data(self, soup: BeautifulSoup):
        table = soup.find('div', attrs={'class': 'epcjfa_content'})
        if table is not None:
            self.gather_top_content(table)
            self.gather_description(table)

    def gather_top_content(self, table: Tag):
        self.title = self.year = self.length = ''
        item_info = table.find('div', attrs={'class': 'epcjfa_topContent'})
        if item_info is not None:
            title_info = item_info.find('h1', attrs={'class': 'epcjfa_title'}).text
            meta_info = item_info.find_all('span')
            meta_text = []
            if meta_info is not None:
                for meta_item in meta_info:
                    meta_text.append(meta_item.text)
        self.title = sanitize_title(title_info)
        self.year = sanitize_year(meta_text[1])
        self.length = parse_length(meta_text[2])
        pass

    def gather_description(self, table):
        self.descr = ''
        item_descr = table.find('p', attrs={'class': 'epcjfa_description'})
        if item_descr is not None:
            self.descr = item_descr.text
        pass

    def print_info(self):

        print(self.url)
        print(self.length)
        print(self.titleWithYear)

        print(valueIfDefinedOrNONE(self.director))
        print(valueIfDefinedOrNONE(self.country))
        print(valueIfDefinedOrNONE(self.stars))
        print(valueIfDefinedOrNONE(self.descr))


    def get_parsed_info(self):
        return [self.title, self.year, self.titleWithYear, self.director, self.country, self.stars,
                self.descr, self.length, self.url]


def main():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    url = ''
    if args.url:
        url = args.url
    movie_parser = SupplementParse(url)
    print('='*54)
    movie_parser.print_info()
    print('='*54)
    print()
    print()


if __name__ == "__main__":
    main()
