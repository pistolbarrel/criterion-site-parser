import json

import requests
from bs4 import BeautifulSoup
import argparse


def extract_title_length(table):
    for item in table.findAll('div', attrs={'class': 'contain margin-top-large column small-16'}):
        return item.h1.text.strip(), item.h5.text.strip()


def extract_info(table):
    info = []
    for item in table.findAll('div', attrs={'class': 'site-font-secondary-color'}):
        for string in item.stripped_strings:
            info.append(string)
    return info


def extract_series_title_feature(soup):
    ret = []
    table = soup.find('li', attrs={'class': 'js-collection-item'})
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = [item.a.text.strip(), item.a['href']]
        ret.append(movie)
    return ret


def valueIfDefinedOrNONE(value):
    return value if value else "NONE"


def establish_table(content):
    soup = BeautifulSoup(content, 'html5lib')
    table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})
    cmsp_length = None
    if not table:
        # desperate attempt to salvage the effort
        cmsp = extract_series_title_feature(soup)
        cmsp_length = cmsp[0][0]
        r = requests.get(cmsp[0][1])
        soup = BeautifulSoup(content, 'html5lib')
        table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})
    return cmsp_length, table


def extract_info_len4(info):
    # hack around episode names for some 'features' and sometimes alternate titles
    if info[0].find('“') >= 0 or info[0].find('(') >= 0:
        diryrcnty = info[1]
        stars = info[2]
        descr = info[3]
        ex_descr = info[0]
    else:
        diryrcnty, stars, descr, ex_descr = info
    country, director, year = process_diryrcnty(diryrcnty)
    descr = descr + '\n\n' + ex_descr
    return country, descr, director, stars, year


def extract_info_len3(info):
    diryrcnty, stars, descr = info
    # hack around episode names for some 'features' and sometimes alternate titles
    if not diryrcnty.find('•') >= 0:
        descr = diryrcnty + "\n\n" + descr
        diryrcnty = stars
        stars = ""

    # sometimes you are here but have no stars listed in the movie.
    # i.e., you have diryrcnty descr1 and descr2. Look for this case
    elif "Starring" not in stars:
        descr = stars + "\n\n" + descr
        stars = ""
    country, director, year = process_diryrcnty(diryrcnty)

    # I know of one instance in the Criterion web site  where the country
    # and year are swapped. It's in the listing for Breathless (1960).
    # This movie is constantly being added to lists. This is a bit of code
    # to fix the issue
    year = year.strip()
    if not year.isnumeric():
        # do a simple swap
        year, country = country, year

    return country, descr, director, stars, year


def extract_info_len2(info):
    country = descr = director = year = ''
    diryrcnty, descr = info
    if '•' in diryrcnty:
        country, director, year = process_diryrcnty(diryrcnty)
    else:
        descr = diryrcnty + '\n\n' + descr
    return country, descr, director, year


def process_diryrcnty(diryrcnty):
    country = director = year = ''
    if '•' in diryrcnty:
        splits = diryrcnty.split('•')
        if len(splits) == 3:
            director, year, country = splits
        if len(splits) == 2:
            year, country = splits
    return country, director, year


def sanitize_data(country, director, length, stars, title, year):
    if stars:
        stars = stars.replace("Starring ", "")
        stars = stars.replace(',', ';')
        stars = stars.strip()

    if title[0:4] == "The ":
        title = title[4:] + ", " + title[0:3]
    if title[0:2] == "A ":
        title = title[2:] + ", " + title[0:1]
    just_title = title

    if year:
        title = title + " (" + year.strip() + ")"
    else:
        title = title + " (NONE)"

    if '•' in length:
        length = length.split('•')[1].strip()

    if director:
        director = director.replace("Directed by ", "")
        director = director.replace(" and ", ",")
        director = director.replace(",", ";")
        director = director.replace(";;", ";")
        director = director.strip()

    if country:
        country = country.replace(',', ';')
        country = country.strip()
    return country, director, length, stars, title, just_title


class MovieParse:
    def __init__(self, url, time_supplied=None):
        self.url = url
        r = requests.get(url)
        cmsp_length, table = establish_table(r.content)
        diryrcnty, stars, descr, director, year, country = '', '', '', '', '', ''
        title, length = extract_title_length(table)
        info = extract_info(table)

        if len(info) == 4:
            country, descr, director, stars, year = extract_info_len4(info)
        if len(info) == 3:
            country, descr, director, stars, year = extract_info_len3(info)
        if len(info) == 2:
            country, descr, director, year = extract_info_len2(info)
        if len(info) == 1:
            descr = info[0]

        country, director, length, stars, title, just_title \
            = sanitize_data(country, director, length, stars, title, year)

        self.length = length
        if cmsp_length:
            self.length = cmsp_length
        if time_supplied:
            self.length = time_supplied
        self.just_title = just_title
        self.title = title
        self.director = director
        self.country = country
        self.stars = stars
        self.descr = descr
        self.year = year.strip()

    def get_parsed_info(self):
        return [self.just_title, self.year, self.title, self.director, self.country, self.stars,
                self.descr, self.length, self.url]

    def print_info(self, supplied_length=None):

        print(self.url)
        if not supplied_length:
            print(self.length)
        print(self.title)
        print('##' + self.title + ' Watched')

        print(valueIfDefinedOrNONE(self.director))
        print(valueIfDefinedOrNONE(self.country))
        print(valueIfDefinedOrNONE(self.stars))
        print(valueIfDefinedOrNONE(self.descr))

    def addViaApi(self, supplied_length=None, collection=None):
        put_uri = "http://localhost:8080/rest/movie"
        movie_dto = {"title": self.just_title,
                     "year": self.year,
                     "actors": self.stars,
                     "directors": self.director,
                     "countries": self.country,
                     "collections": collection,
                     "description": self.descr}
        movie_length = self.length
        if supplied_length:
            movie_length = supplied_length
        movie_dto["duration"] = movie_length

        # print the json instead of calling api
        print(json.dumps(movie_dto))
        # response = requests.put(put_uri, json=movie_dto)
        # if response.status_code != 200:
        #     print("Error")


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
