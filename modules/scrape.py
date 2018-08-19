import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import urlparse
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def scrapepage(url):
    '''given a url, return document links matching the URL's domain'''
    urls = []
    ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    extensions = ['docx','pptx','pdf','xlsx', 'doc', 'ppt', 'xls']
    r = requests.get(url,headers=ua,allow_redirects=True,verify=False)
    soup = BeautifulSoup(r.content,'html.parser')
    for link in soup.find_all('a'):
        link = link.get('href')
        link = urlparse.urljoin(url, link)
        if link.split('.')[-1] in extensions:
            '''if parent domain of url is the same as the link, save it - this should handle subdomains'''
            ls = urlparse.urlparse(link).netloc.split('.')
            ls = ls[-2] + '.' + ls[-1]

            us = urlparse.urlparse(url).netloc.split('.')
            us = us[-2] + '.' + us[-1]

            if ls == us:
                urls.append(link)

    return urls
