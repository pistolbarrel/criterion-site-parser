import json
from collections import namedtuple


def call_api(movies_list, series_name):
    MovieInfo = namedtuple("MovieInfo", "just_title year title director country stars descr length url")
    episode = 0
    for movie in movies_list:
        episode += 1
        time, url, title = movie
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, 'html5lib')
        # url_type = CriterionParser.determine_url_type(soup)
        # if url_type == 'collection':
        #     time, url = CriterionParser.extract_collection_title_feature(soup)[0]
        # movie_parser = CriterionMovieParse.MovieParse(url)
        addViaApi(movie, time, series_name)


def addViaApi(movie, supplied_length=None, collection=None):
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
