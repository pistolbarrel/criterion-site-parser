import json

from critparse import CriterionParser


def test_new_determine_url_type_collection():
    url = "https://www.criterionchannel.com/collections/JKc7wng3/rock-biopics-that-don-t-suck"
    one = CriterionParser.CriterionParser.determine_url_type(url)
    assert one == 'collection'


def test_new_determine_url_type_none(soup_none):
    url = "https://www.criterionchannel.com/series/q9n77HtL/neon-genesis-evangelion"
    one = CriterionParser.CriterionParser.determine_url_type(url)
    assert one is None


def test_extract_movie_info_from_movie_page(soup_new_movie):
    table = soup_new_movie.find('p', attrs={'class': 'Hero-module-less-module__epcjfa__description'})
    if table is not None:
        print(table.text)
    table = soup_new_movie.find('main', attrs={'class': 'main-content'})
    for item in table.contents:
        if item.string is None:
            continue
        if 'director' in item.string:
            data_dict = json.loads(item.string)
            for director in data_dict['director']:
                print(director['name'])
        if 'countryOfOrigin' in item.string:
            data_dict = json.loads(item.string)
            print(data_dict['countryOfOrigin'])
        assert True

def test_gather_urls_of_collection(soup_new_collection):
    print(soup_new_collection.title.text)
    table = soup_new_collection.find('ul', attrs={'class': 'CardRail-module-less-module__P8X20G__grid'})
    for title in table.contents:
        hel = title.find('a', attrs={'class': 'PlaylistCard-module-less-module__Xfr99W__overlayLink' })
        if hel is not None:
            print(hel['href'])
            pass
        hel2 = title.find('img', attrs={'class':'CardImage-module-less-module__vvKVuW__image lazyload'})
        if hel2 is not None:
            print(hel2['alt'])

def test_gather_urls_of_edition(soup_new_edition):
    print(soup_new_edition.title.text)
    table = soup_new_edition.find('ul', attrs={'class': 'CardRail-module-less-module__P8X20G__grid'})
    for title in table.contents:
        hel = title.find('a', attrs={'class': 'PlaylistCard-module-less-module__Xfr99W__overlayLink' })
        if hel is not None:
            print(hel['href'])
            pass

# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================
