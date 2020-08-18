#
from .scraper import Scraper
from .. import RateLimited

import base64
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('lyricscraper')

class MusixMatchScraper(Scraper):
    """ Pulls lyrics from MusixMatch """
    BASE_URL = 'https://www.musixmatch.com'
    QUERY_URL = 'https://www.musixmatch.com/artist/%s' # Query parameters (Oliver-Tree)
    
    def __init__(self):
        super().__init__()
        
    def name(self):
        return 'MusixMatch'
    
    @RateLimited(1) # Limit at 1 calls per second
    def scrape(self, song):
        query = song.artist.replace(' ', '-')
        url = self.QUERY_URL % query
        
        logger.info('[MusixMatch] Searching for {}'.format(url))
        
        search_results = requests.get(url, headers=self.request_headers).content
        soup = BeautifulSoup(search_results, 'html.parser')
        
        lyrics = ''
        
        # Validate results found
        if soup.find('div', {'class': 'error-page'}) is not None:
            logger.info('[MusixMatch] No match found')
            return lyrics
        
        
        for a in soup.find('ul', {'class': 'tracks list'}).find_all('a', {'class': 'title'}):
            for song_title in a.findChildren('span'):
                if song_title.text is not None and song.title in song_title.text:
                    song_url = self.BASE_URL + a.get('href')
                    search_results = requests.get(song_url, headers=self.request_headers).content
                    lyric_soup = BeautifulSoup(search_results, 'html.parser') # TODO: Switch out with lxml
                    
                    
                    for block in lyric_soup.find_all('span', {'class': 'lyrics__content__ok'}):
                        if block is not None:
                            lyrics += '\n' + block.text
                    
                    return lyrics
        
        # Clean up lyrics
        return lyrics
