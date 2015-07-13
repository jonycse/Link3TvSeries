__author__ = 'AbuZahedJony'
from requests import session
import utils

from pprint import pprint
from bs4 import BeautifulSoup
import time, re, os

from config import *

# use RANGE_UPPER, RANGE_LOWER for download tv series by range
# use -99999, 99999 for ignore
RANGE_LOWER = -99999
RANGE_UPPER = 99999

class Link3TvSeriesDownloader:

    def __init__(self, df='files', download_url = None, username='user', password='user1234'):
        self.URL_TV_SERIES = download_url
        self.TV_SERIES_DOWNLOAD_FOLDER = df
        self.username = username
        self.password = password

        self._do_initial_setup()
        self._do_initial_task()


    def _do_initial_setup(self):
        self.TV_SERIES_DOWNLOAD_BASE_FOLDER = 'downloads'
        self.urlLogin = 'http://www.cinehub24.com/auth/login'
        self.download_path = self.TV_SERIES_DOWNLOAD_BASE_FOLDER+'/'+self.TV_SERIES_DOWNLOAD_FOLDER+'/'
        self.payload = {
            'action': 'login',
            'user_name': self.username,
            'user_password': self.password,
            'doLogin': True
        }

    def _do_initial_task(self):
        self._create_directory(self.download_path)

    def process(self):
        print "Parsing TV series: "
        if self.URL_TV_SERIES is None:
            print "No url found"
            return
        with session() as c:
            final_results = []
            c.post(self.urlLogin, data=self.payload)
            #urlTVSeries = 'http://www.cinehub24.com/item/tvseries/english-tv-program/castle-season-7-updated-every-week.aspx'
            urlTVSeries = self.URL_TV_SERIES
            print "Url",urlTVSeries
            response = c.get(urlTVSeries)
            html = response.text
            links =  self.parse_tv_series(html, c)
            total_files_for_download = len(links)
            k = 1
            for link in links:
                # If you want to apply range, uncomment this block
                #if not (k>=RANGE_LOWER and k<=RANGE_UPPER):
                #    print "K",k,"Range break"
                #    k += 1
                #    continue

                print "Downloading", k, "of", total_files_for_download
                link = link.encode('utf-8')
                #print 'Link', str(link)
                utils.download_file(link, self.download_path, BLOCK_SIZE)
                k += 1

    def parse_tv_series(self, html, c):
        results = []
        soup = BeautifulSoup(html)
        a = soup.find_all('table', id = 'travel')
        episodes_lis_table = a[0]
        k = 0
        for row in episodes_lis_table.find_all('tr'):
            k+=1
            if k<2:
                continue
            m = 0
            for td in row.find_all('td'):
                m += 1
                if m == 5:
                    download_page = td.a.get('href')
                    #print download_page
                    download_file_response = c.get(download_page)
                    html_download_file = download_file_response.text
                    url = self.get_download_url(html_download_file)
                    results.append(url)
                    #break
            #break

        return results


    @staticmethod
    def _create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def get_download_url(html):
        soup = BeautifulSoup(html)
        a = soup.find_all('div', id = 'download')
        download_tree = a[0]
        download_tag = download_tree.p.input
        #pprint(download_tag)
        return download_tag.get('value')


# Main for script
if __name__=='__main__':
    print "Running link3 TV series downloader ......."
    link3TvSeriesDownloader= Link3TvSeriesDownloader(SAVED_FOLDER_NAME, TV_SERIES_URL, USER_NAME, PASSWORD)
    link3TvSeriesDownloader.process()

'''
# Main for exe
if __name__=='__main__':
    print "\nPlease make sure give each input as string (use double quotes)\n"
    URL = input("Enter TV series URL(example \"www.google.com\"):")
    un = input("Enter username(example \"myname\"):")
    ps = input("Enter password:(example \"mypassword\")")
    download_folder = input("Enter download folder name:(example \"downloads\")")

    link3TvSeriesDownloader= Link3TvSeriesDownloader(download_folder, URL, un, ps)
    link3TvSeriesDownloader.process()
'''