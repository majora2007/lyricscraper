from .scraper import Scraper
from .. import RateLimited
from .. import webdriver

import base64
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('lyricscraper')

class GeniusScraper(Scraper):
    """ Pulls lyrics from Genius """

    QUERY_URL = 'https://genius.com/search?q=%s' # https://genius.com/search?q=Watsky%20-%20Don%27t%20be%20nice
    driver = None
    
    def __init__(self):
        super().__init__()
        self.driver = webdriver.WebDriver()
        
    def name(self):
        return 'Genius'
    
    @RateLimited(1) 
    def scrape(self, song,):
        self.driver.init_chrome()
        
        query = song.artist + ' - ' + song.title
        url = self.QUERY_URL % query
        lyrics = ''
        
        logger.info('[Genius] Searching for {}'.format(url))
        
        self.driver.get_url(url)
        
        # Validate results found
        try:
            if self.driver.verify_elem('div[ng-if="$ctrl.sections && !$ctrl.has_results"]'):
                logger.info('[Genius] No match found')
                return lyrics
        except:
            pass
        
        for a in self.driver.verify_elems('a.mini_card'):
            soup = BeautifulSoup(a.get_attribute('innerHTML'), 'html.parser')

            artist = self.clean(soup.find('div', {'class': 'mini_card-subtitle'}).text).lower()
            title = self.clean(soup.find('div', {'class': 'mini_card-title'}).text).lower()
            
            if artist == song.artist.strip().lower() and title == song.title.strip().lower():
                search_results = requests.get(a.get_attribute('href'), headers=self.request_headers).content
                lyric_soup = BeautifulSoup(search_results, 'html.parser') # TODO: Switch out with lxml
                
                lyrics = lyric_soup.find('p').text
                break
        
        self.driver.close()
        
        # Clean up lyrics
        return lyrics

    def clean(self, title):
        """ Clean things like ’ -> ' """
        return title.strip().replace('’', '\'')