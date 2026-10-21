import requests
from bs4 import BeautifulSoup
import argparse
from critparse import CriterionParser, CriterionMovieParse, OutText


# https:\\www.criterionchannel.com

class CriterionParser:
    """Main Class for the collection of movie data from the Criterion Channel
    (www.criterionchannel.com)

    Two different 'views' are currently implemented to display the collected
    data. One is a test representation of the data, the other is a Json
    representation of the data. The former is what I've been using for a couple
    of years to manage my movie viewing. The latter is interfacing with a rest
    interface of a database of my movies.

    Usage:
        parser = CriterionParser(url)      // instantiate the class
        parser.gather_all_info()           // gather the data
        TextOut.movie_info_to_text(parser) // present the data
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html5lib')
        # collect test content here from response.content
        self.url_type = CriterionParser.determine_url_type(self.url)
        print("url has been determined to be: " + str(self.url_type))
        print()
        self.series_name = ''
        self.all_movie_parsed_data = []
        self.time = None
        self.extracted_episode_info = None
        self.description = None

    def gather_all_info(self, args):
        """
        Main driver method and entry point into data gathering.

        :return: None
        """
        if self.url_type == 'movie':
            self.gather_movie_list_info([[self.url, ""]])

        elif self.url_type == 'collection':
            self.series_name, self.extracted_episode_info = CriterionParser.get_collection_info(self.soup)
            self.gather_movie_list_info(self.extracted_episode_info)

    def gather_movie_list_info(self, movies_list):
        """
        This gathers one or more movies' data from the list of movies provided as an argument.

        :param movies_list: List of individual movie urls.

        :return: None
        """
        for movie in movies_list:
            url = movie[0]
            if '/series/' in url:
                continue
            movie_parser = CriterionMovieParse.MovieParse(movie[0])
            self.all_movie_parsed_data.append(movie_parser.get_parsed_info())

    def __explore_possible_collections(self, movies_list):
        """
        This experimental feature attempts to guess a 'collection's url from
        the url obtained in the movies_list. Using this, and a call to
        get_collection_info, it will see if the movie has a collection of videos.

        :param movies_list: List of individual movie information. List required
            to be a minimum of len(2)

        :return: None
        """
        print('Discovering collections ...')
        for movie in movies_list:
            url = self.guess_collection_url(movie[1])
            if url == self.url:
                continue
            response = requests.get(url)
            if response.status_code != 200:
                url = url + '-1'
                response = requests.get(url)
                if response.status_code != 200:
                    print('Trouble with request of: ' + url + ". Giving up.")
                    continue
            soup = BeautifulSoup(response.content, 'html5lib')
            series_name, series = CriterionParser.get_collection_info(soup)
            if len(series) > 1:
                # got a live one!
                if len(series) >= 4:
                    print("'" + series_name + "' has " + str(len(series)) + " videos.")
                else:
                    s = "','"
                    transposed_series = list(zip(*series))
                    titles = "'" + s.join(transposed_series[2]) + "'"
                    print("'" + series_name + "' has " + str(len(series)) + " videos -- " + titles)
        print()

    @staticmethod
    def get_collection_info(soup):
        """
        Parses and extracts the collection information. By collection I mean a loose coupling for
        a movie or a list of movies. More and more single movies tend to have a 'front door' page
        where you can read the full description without the movie starting.

        :param soup: instance to search/parse

        :return: tuple containing series_name and episode_info (a list of lists)
        """
        series = []
        url = imgTitle = ''
        collectionTitle = soup.title.text
        index = collectionTitle.find(' |')
        if index != -1:
            collectionTitle = collectionTitle[:index]
        series_name = "Criterion:" + collectionTitle

        table = soup.find('ul', attrs={'class': 'CardRail-module-less-module__P8X20G__grid'})
        for card in table.contents:
            url = imgTitle = ''
            itemUrl = card.find('a', attrs={'class': 'PlaylistCard-module-less-module__Xfr99W__overlayLink'})
            if itemUrl is not None:
                url = 'https://www.criterionchannel.com' + itemUrl['href']
            itemImgTitle = card.find('img', attrs={'class': 'CardImage-module-less-module__vvKVuW__image lazyload'})
            if itemImgTitle is not None:
                imgTitle = itemImgTitle['alt']

            series.append([url, imgTitle])


        return series_name, series

    @staticmethod
    def determine_url_type(url):
        """
        Determines the type of url of the soup instance. At the present time,
        I don't know how to deal with a series -- like a television program
        with seasons and episodes.

        Criterion Edition is less "defined" in the new web presentation.
        Might have to figure this out as we go.

        :param soup: instance to search/parse

        :return:
            None represents a series.
            "movie" represents a movie link.
            "collection" represents a collection of movies.
        """
        if 'films' in url:
            return 'movie'
        elif 'collection' in url or 'discover' in url:
            return 'collection'
        else:
            return  None


def main():
    args = process_args()
    if args.url:
        parser = CriterionParser(args.url)
        parser.gather_all_info(args)
        OutText.movie_info_to_text(parser.url_type, parser.series_name, parser.description,
                                   parser.all_movie_parsed_data)


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-a", "--api", help="Add movie via REST api", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
