import argparse
from critparse import CriterionParser, TextOut
from collections import namedtuple


def main():
    args = process_args()
    if args.url:
        if args.api:
            parser = CriterionParser.CriterionParser(args.url)
            parser.collect_information_for_api()
        else:
            # parser = CriterionParser.CriterionParser(args.url)
            # parser.print_info()
            # print("$" * 100)
            # print("$" * 100)
            # print("$" * 100)
            parser = CriterionParser.CriterionParser(args.url)
            parser.gather_all_info()
            TextOut.movie_info_to_text(parser)


            # parser.print_info()
            # parser.print_info()
            a = 42

def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-a", "--api", help="Add movie via REST api", action='store_true')
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    main()
