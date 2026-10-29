import json

import requests
from bs4 import BeautifulSoup
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
    return year[0:4]


def sanitize_length(length):
    hours = minutes = seconds = '00'

    length = length[2:] # strip the 'PT'
    index = length.find('H')
    if index != -1:
        hours = length[:index]
        length = length[index + 1:]
    index = length.find('M')
    if index != -1:
        minutes = length[:index]
        minutes = "0" + minutes
        minutes = minutes[-2:]
        length = length[index + 1:]
    index = length.find('S')
    if index != -1:
        seconds = length[:index]
        seconds = "0" + seconds
        seconds = seconds[-2:]

    if '00' not in hours:
        return hours + ':' + minutes + ':' + seconds
    else:
        return minutes + ':' + seconds


def santize_title(title):
    if title[0:4] == "The ":
        title = title[4:] + ", " + title[0:3]
    if title[0:2] == "A ":
        title = title[2:] + ", " + title[0:1]
    title = title.replace(";", "_")
    return title

class MovieParse:
    def __init__(self, url, time_supplied=None):
        self.url = url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        self.director = ''
        self.collect_movie_data(soup)

        self.title = santize_title(self.title)
        self.year = sanitize_year(self.year)
        self.length = sanitize_length(self.length)
        self.titleWithYear = self.title + ' (' + self.year + ')'

    def collect_movie_data(self, soup: BeautifulSoup):
        table = soup.find('p', attrs={'class': 'epcjfa_description'})
        if table is not None:
            self.descr = table.text
        table = soup.find('main', attrs={'class': 'main-content'})
        for item in table.contents:
            if item.string is None:
                continue
            if '"director"' in item.string:
                self.director = extract_director(item)
            if 'countryOfOrigin' in item.string:
                self.country = extract_country(item)
                self.stars = extract_stars(item)
                self.title, self.year, self.length = extract_title_year_length(item)

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
    movie_parser = MovieParse(url)
    print('='*54)
    movie_parser.print_info()
    print('='*54)
    print()
    print()


if __name__ == "__main__":
    main()
