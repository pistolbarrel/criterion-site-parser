from critparse import CriterionParser


def test_extract_next_url_collection(soup_collection):
    expected_url = None
    url = CriterionParser.CriterionParser.extract_next_url(soup_collection)
    assert expected_url == url


def test_extract_next_url_unusual(soup_unusual_collection):
    expected_url = None
    url = CriterionParser.CriterionParser.extract_next_url(soup_unusual_collection)
    assert expected_url == url


def test_extract_next_url_none(soup_none):
    expected_url = None
    url = CriterionParser.CriterionParser.extract_next_url(soup_none)
    assert url == expected_url


def test_determine_url_type_collection(soup_collection):
    one = CriterionParser.CriterionParser.determine_url_type(soup_collection)
    assert one == 'collection'


def test_determine_url_type_special_sub(soup_special_subtitle):
    one = CriterionParser.CriterionParser.determine_url_type(soup_special_subtitle)
    assert one == 'movie'


def test_determine_url_type_none(soup_none):
    one = CriterionParser.CriterionParser.determine_url_type(soup_none)
    assert one is None


def test_determine_url_type_collection(soup_collection):
    one = CriterionParser.CriterionParser.determine_url_type(soup_collection)
    assert one is 'collection'


def test_extract_collection_name_and_description_collection(soup_collection):
    one, two = CriterionParser.CriterionParser.extract_collection_name_and_description(soup_collection)
    assert one == 'The Front Page'
    assert two == 'Starring Adolphe Menjou, Pat O’Brien, Mary Brian'


def test_extract_collection_name_and_description_coll_dir(soup_collection_director):
    one, two = CriterionParser.CriterionParser.extract_collection_name_and_description(soup_collection_director)
    assert one == 'La Jetée'
    assert two == 'Directed by Chris Marker • 1963 • France'


def test_extract_collection_name_and_description_special_sub(soup_special_subtitle):
    one, two = CriterionParser.CriterionParser.extract_collection_name_and_description(soup_special_subtitle)
    assert one == 'NoName'
    assert two == 'NoDescription'


def test_extract_collection_name_and_description_none(soup_none):
    one, two = CriterionParser.CriterionParser.extract_collection_name_and_description(soup_none)
    assert one == 'Three by Jafar Panahi'
    assert two == 'The brilliant Iranian auteur Jafar Panahi was sentenced to six years in prison in July 2022, after refusing to stop making urgent, perceptive films when he was banned from the profession in 2010. With NO BEARS, his latest film, coming out in December, there’s no better time to revisit three of his most beloved masterpieces, all of which view modern Iran through the eyes of young girls.'


def test_extract_collection_name_and_description_unusual(soup_unusual_collection):
    one, two = CriterionParser.CriterionParser.extract_collection_name_and_description(soup_unusual_collection)
    assert one == 'The Organizer'
    assert two == 'Starring Marcello Mastroianni, Renato Salvatori, Annie Girardot'


def test_extract_title_feature_collection(soup_collection):
    expected = [['1:41:27', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page', 'NoTitle']]
    ret = CriterionParser.CriterionParser.extract_title_feature_from_collection(soup_collection)
    assert ret == expected


def test_extract_title_feature_special_sub(soup_special_subtitle):
    expected = [['1:21:40',
  'https://www.criterionchannel.com/foreign-language-oscar-winners/season:1/videos/war-and-peace-part-3',
  'NoTitle']]
    ret = CriterionParser.CriterionParser.extract_title_feature_from_collection(soup_special_subtitle)
    assert ret == expected


def test_extract_title_feature_none(soup_none):
    expected = [['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon', 'NoTitle']]
    ret = CriterionParser.CriterionParser.extract_title_feature_from_collection(soup_none)
    assert ret == expected


def test_extract_title_feature_unusual(soup_unusual_collection):
    expected = [['2:09:54', 'https://www.criterionchannel.com/the-organizer/videos/the-organizer', 'NoTitle']]
    ret = CriterionParser.CriterionParser.extract_title_feature_from_collection(soup_unusual_collection)
    assert ret == expected


def test_extract_episode_time_and_url_collection(soup_collection):
    expected = [['24:04', 'https://www.criterionchannel.com/the-front-page/videos/restoring-the-front-page',
                 'Restoring THE FRONT PAGE'], ['25:47',
                                               'https://www.criterionchannel.com/the-front-page/videos/david-brendel-on-screenwriter-ben-hecht',
                                               'David Brendel on Screenwriter Ben Hecht'],
                ['58:47', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1937',
                 'THE FRONT PAGE Radio Adaptation: 1937'],
                ['31:44', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1946',
                 'THE FRONT PAGE Radio Adaptation: 1946']]
    ret = CriterionParser.CriterionParser.extract_episode_time_and_url(soup_collection)
    assert ret == expected


def test_extract_episode_time_and_url_special_sub(soup_special_subtitle):
    expected = []
    ret = CriterionParser.CriterionParser.extract_episode_time_and_url(soup_special_subtitle)
    assert ret == expected


def test_extract_episode_time_and_url_none(soup_none):
    expected = [['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon', 'The White Balloon'], ['1:34:33', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-mirror-1', 'The Mirror'], ['1:31:46', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/offside', 'Offside']]
    ret = CriterionParser.CriterionParser.extract_episode_time_and_url(soup_none)
    assert ret == expected


def test_extract_episode_time_and_url_unusual(soup_unusual_collection):
    expected = [['06:03', 'https://www.criterionchannel.com/the-organizer/videos/spotlight-on-the-organizer-with-imogen-sara-smith', 'Spotlight on THE ORGANIZER with Imogen Sara Smith'], ['10:38', 'https://www.criterionchannel.com/the-organizer/videos/mario-monicelli', 'Mario Monicelli on THE ORGANIZER']]
    ret = CriterionParser.CriterionParser.extract_episode_time_and_url(soup_unusual_collection)
    assert ret == expected


def test_guess_collection_url():
    url = 'https://www.criterionchannel.com/something-different/videos/something-different'
    expected = 'https://www.criterionchannel.com/something-different'
    result = CriterionParser.CriterionParser.guess_collection_url(url)
    assert result == expected


def test_get_collection_info_collection(soup_collection):
    expected_name = 'Collection:The Front Page'
    expected_series = [['1:41:27', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page', 'NoTitle'],
                       ['24:04', 'https://www.criterionchannel.com/the-front-page/videos/restoring-the-front-page',
                        'Restoring THE FRONT PAGE'], ['25:47',
                                                      'https://www.criterionchannel.com/the-front-page/videos/david-brendel-on-screenwriter-ben-hecht',
                                                      'David Brendel on Screenwriter Ben Hecht'], ['58:47',
                                                                                                   'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1937',
                                                                                                   'THE FRONT PAGE Radio Adaptation: 1937'],
                       ['31:44',
                        'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1946',
                        'THE FRONT PAGE Radio Adaptation: 1946']]

    name, series = CriterionParser.CriterionParser.get_collection_info(soup_collection)
    assert name == expected_name
    assert series == expected_series


def test_get_collection_info_special_sub(soup_special_subtitle):
    expected_name = 'Collection:NoName'
    expected_series = [['1:21:40',
  'https://www.criterionchannel.com/foreign-language-oscar-winners/season:1/videos/war-and-peace-part-3',
  'NoTitle']]

    name, series = CriterionParser.CriterionParser.get_collection_info(soup_special_subtitle)
    assert name == expected_name
    assert series == expected_series


def test_get_collection_info_none(soup_none):
    expected_name = 'Collection:Three by Jafar Panahi'
    expected_series = [
        ['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon',
         'NoTitle'],
        ['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon',
         'The White Balloon'],
        ['1:34:33', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-mirror-1',
         'The Mirror'],
        ['1:31:46', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/offside', 'Offside']]

    name, series = CriterionParser.CriterionParser.get_collection_info(soup_none)
    assert name == expected_name
    assert series == expected_series


def test_get_collection_info_unusual(soup_unusual_collection):
    expected_name = 'Collection:The Organizer'
    expected_series = [['2:09:54', 'https://www.criterionchannel.com/the-organizer/videos/the-organizer', 'NoTitle'], ['06:03', 'https://www.criterionchannel.com/the-organizer/videos/spotlight-on-the-organizer-with-imogen-sara-smith', 'Spotlight on THE ORGANIZER with Imogen Sara Smith'], ['10:38', 'https://www.criterionchannel.com/the-organizer/videos/mario-monicelli', 'Mario Monicelli on THE ORGANIZER']]

    name, series = CriterionParser.CriterionParser.get_collection_info(soup_unusual_collection)
    assert name == expected_name
    assert series == expected_series


def test_get_edition_info_collection(soup_collection):
    expected_name = 'The Front Page'
    expected_series = [['1:41:27', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page', 'NoTitle'],
                       ['24:04', 'https://www.criterionchannel.com/the-front-page/videos/restoring-the-front-page',
                        'Restoring THE FRONT PAGE'], ['25:47',
                                                      'https://www.criterionchannel.com/the-front-page/videos/david-brendel-on-screenwriter-ben-hecht',
                                                      'David Brendel on Screenwriter Ben Hecht'], ['58:47',
                                                                                                   'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1937',
                                                                                                   'THE FRONT PAGE Radio Adaptation: 1937'],
                       ['31:44',
                        'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1946',
                        'THE FRONT PAGE Radio Adaptation: 1946']]

    name, series = CriterionParser.CriterionParser.get_edition_info(soup_collection)
    assert name == expected_name
    assert series == expected_series


def test_get_edition_info_special_sub(soup_special_subtitle):
    expected_name = 'NoName'
    expected_series = [['1:21:40',
  'https://www.criterionchannel.com/foreign-language-oscar-winners/season:1/videos/war-and-peace-part-3',
  'NoTitle']]

    name, series = CriterionParser.CriterionParser.get_edition_info(soup_special_subtitle)
    assert name == expected_name
    assert series == expected_series


def test_get_edition_info_none(soup_none):
    expected_name = 'Three by Jafar Panahi'
    expected_series = [
        ['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon',
         'NoTitle'],
        ['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon',
         'The White Balloon'],
        ['1:34:33', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-mirror-1',
         'The Mirror'],
        ['1:31:46', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/offside', 'Offside']]

    name, series = CriterionParser.CriterionParser.get_edition_info(soup_none)
    assert name == expected_name
    assert series == expected_series


def test_get_series_info_collection(soup_collection):
    expected_name = 'Criterion:The Front Page'
    expected_descr = 'Starring Adolphe Menjou, Pat O’Brien, Mary Brian'
    expected_series = [['24:04', 'https://www.criterionchannel.com/the-front-page/videos/restoring-the-front-page', 'Restoring THE FRONT PAGE'], ['25:47', 'https://www.criterionchannel.com/the-front-page/videos/david-brendel-on-screenwriter-ben-hecht', 'David Brendel on Screenwriter Ben Hecht'], ['58:47', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1937', 'THE FRONT PAGE Radio Adaptation: 1937'], ['31:44', 'https://www.criterionchannel.com/the-front-page/videos/the-front-page-radio-adaptation-1946', 'THE FRONT PAGE Radio Adaptation: 1946']]

    name, descr, series = CriterionParser.CriterionParser.get_series_info(soup_collection)
    assert name == expected_name == name
    assert descr == expected_descr
    assert series == expected_series


def test_get_series_info_special_sub(soup_special_subtitle):
    expected_name = 'Criterion:NoName'
    expected_descr = 'NoDescription'
    expected_series = []

    name, descr, series = CriterionParser.CriterionParser.get_series_info(soup_special_subtitle)
    assert name == expected_name == name
    assert descr == expected_descr
    assert series == expected_series


def test_get_series_info_none(soup_none):
    expected_name = 'Criterion:Three by Jafar Panahi'
    expected_descr = 'The brilliant Iranian auteur Jafar Panahi was sentenced to six years in prison in July 2022, after refusing to stop making urgent, perceptive films when he was banned from the profession in 2010. With NO BEARS, his latest film, coming out in December, there’s no better time to revisit three of his most beloved masterpieces, all of which view modern Iran through the eyes of young girls.'
    expected_series = [
        ['1:24:49', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-white-balloon',
         'The White Balloon'],
        ['1:34:33', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/the-mirror-1',
         'The Mirror'],
        ['1:31:46', 'https://www.criterionchannel.com/three-by-jafar-panahi/season:1/videos/offside', 'Offside']]

    name, descr, series = CriterionParser.CriterionParser.get_series_info(soup_none)
    assert name == expected_name == name
    assert descr == expected_descr
    assert series == expected_series

# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================
