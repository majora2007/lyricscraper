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
        query = song.artist.strip().replace(' ', '-')
        url = self.QUERY_URL % query
        
        logger.info('\t[MusixMatch] Searching for {}'.format(url))
        
        search_results = requests.get(url, headers=self.request_headers).content
        soup = BeautifulSoup(search_results, 'html.parser')
        
        lyrics = ''
        
        # Validate results found
        try:
            if soup.find('div', {'class': 'error-page'}) is not None:
                logger.debug('[MusixMatch] No match found')
            return lyrics
        except:
            pass
        
        # TODO: Need to click Load More button: <a href="/artist/Math-the-Band/3" class="button page-load-more" data-page="3">Load more</a> (requires JS)
        # Seems we can incremenet the number https://www.musixmatch.com/artist/Math-the-Band/1...100
        # This requires many requests though and seems to go way more than it should. Perhaps we should use album from tag to quickly find song
        # ie) https://www.musixmatch.com/artist/Math-the-Band/albums
        
        for a in soup.find('ul', {'class': 'tracks list'}).find_all('a', {'class': 'title'}):
            for song_title in a.findChildren('span'):
                if song_title.text is not None and song.title in song_title.text:
                    song_url = self.BASE_URL + a.get('href')
                    search_results = requests.get(song_url, headers=self.request_headers).content
                    lyric_soup = BeautifulSoup(search_results, 'html.parser') # TODO: Switch out with lxml (looks like lxml is default, just need to have in requirements)
                    
                    
                    for block in lyric_soup.find_all('span', {'class': 'lyrics__content__ok'}):
                        if block is not None:
                            lyrics += '\n' + block.text
                    
                    return lyrics
        
        # Clean up lyrics
        return lyrics
