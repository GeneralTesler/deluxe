import argparse

BANNER='''       ___       ___
      /  /      /  /    @2xxeformyshirt
  ___/  /______/  /_________ __________
 / _   /  /___/  /   /  /\  /  /  /___/
/_____/______/__/______/__,\__/______/
'''

'''parent parser'''
parser = argparse.ArgumentParser(prog='deluxe')
subparsers = parser.add_subparsers(dest='sps')

'''subparsers'''
parser_search = subparsers.add_parser('search',
                                    help='search Google for files')
parser_scrape = subparsers.add_parser('scrape',
                                    help='scrape a site for files')
parser_extact = subparsers.add_parser('extract',
                                    help='extract metadata from files')

'''search arguments'''
parser_search.add_argument('-d',
                            dest='domain',
                            type=str,
                            required=True,
                            help='target domain')
parser_search.add_argument('-n',
                            dest='numres',
                            type=int,
                            required=False,
                            default=25,
                            help='approx. number of search results to retrieve (per extension)')
parser_search.add_argument('-o',
                            dest='searchout',
                            type=str,
                            required=True,
                            help='output directory for files')

'''scrape arguments'''
parser_scrape.add_argument('-u',
                            dest='url',
                            type=str,
                            required=True,
                            help='page to scrape')
parser_scrape.add_argument('-o',
                            dest='scrapeout',
                            type=str,
                            required=True,
                            help='output directory for files')

'''extract arguments'''
parser_extact.add_argument('-m',
                            dest='man',
                            type=str,
                            required=True,
                            help='manifest file location')
parser_extact.add_argument('-o',
                            dest='extout',
                            type=str,
                            required=True,
                            help='output file name')
parser_extact.add_argument('-p',
                            '--print',
                            dest='print',
                            action='store_true',
                            required=False,
                            help='print CSV of results to terminal')

