import argparse
from critparse import CriterionParser, OutText, OutApi


def main():
    """
    This is the (true) main of the critparse module.
    """
    args = process_args()
    if args.url:
        parser = CriterionParser.CriterionParser(args.url)
        parser.gather_all_info(args)
        if args.api:
            OutApi.call_api(parser.all_movie_parsed_data, parser.series_name, args.quiet)
        if not args.noprint:
            print('Examined ' + parser.url)
            OutText.movie_info_to_text(parser.url_type, parser.series_name, parser.description,
                                       parser.all_movie_parsed_data, parser.extracted_episode_info)


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-n", "--noprint", help="Suppress printing the movie info", action='store_true')
    parser.add_argument("-a", "--api", help="Add movie via REST api", action='store_true')
    parser.add_argument("-s", "--skipdiscovery", help="Skip the discovery of collections", action='store_true')
    parser.add_argument("-q", "--quiet", help="Suppress the printing of the title of each movie as it is added",
                        action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
