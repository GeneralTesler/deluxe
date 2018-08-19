import sys,json
import modules.search as Searcher
import modules.scrape as Scraper
import modules.extract as Extractor
import modules.download as Downloader
import modules.args as ArgumentHandler

__author__ = '@2xxeformyshirt'
__version__ = '1.0.0'

if len(sys.argv) == 1:
    print '[-] Missing arguments...quitting!'
    sys.exit()

def extract(args):
    '''extract metadata from files listed in manifest'''
    print '[+] Extracting metadata from documents specified in \033[1m%s\033[0m' % args['man']
    manj = Extractor.processmanifest(args['man'],args['extout'])
    print '[+] Updated manifest written to \033[1m%s\033[0m' % args['extout']
    if args['print']:
        print '[+] Printing CSV of results to terminal\n'
        Extractor.pprintmanifest(manj)

def scrape(args):
    '''given a url, download a list of links'''
    print '[+] Scraping \033[1m%s\033[0m for document links' % args['url']
    urls = Scraper.scrapepage(args['url'])
    print '[+] Downloading identified documents to \033[1m%s\033[0m' % args['scrapeout']
    Downloader.downloadlist(urls,args['scrapeout'])
    print '[+] Manifest written to \033[1m%s/manifest.json\033[0m' % args['scrapeout']

def search(args):
    '''given a domain, download a list of links'''
    print '[+] Searching Google for document links for \033[1m%s\033[0m' % args['domain']
    urls = Searcher.extensionsearch(args['domain'],args['numres'])
    print '[+] Downloading identified documents to \033[1m%s\033[0m' % args['searchout']
    Downloader.downloadlist(urls,args['searchout'])
    print '[+] Manifest written to \033[1m%s/manifest.json\033[0m' % args['searchout']

def main():
    print ArgumentHandler.BANNER
    args = vars(ArgumentHandler.parser.parse_args())
    
    '''switch on subparser'''
    if args['sps'] == 'extract':
        extract(args)
    elif args['sps'] == 'scrape':
        scrape(args)
    elif args['sps'] == 'search':
        search(args)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '[-] User interrupt...quitting!'
        sys.exit()
