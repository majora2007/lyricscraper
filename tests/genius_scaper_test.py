import unittest
import os
import time

import lyricscraper.scrapers.genius_scraper
import lyricscraper.song

class TestGeniusScraper(unittest.TestCase):
    
    start_time = 0
    end_time = 0
    scapper = lyricscraper.scrapers.genius_scraper.GeniusScraper()
    
    def setUp(self):
        self.start_time = time.time()
    
    def tearDown(self):
        self.end_time = time.time()
        print('{} took {} to execute'.format(self.id(), (self.end_time - self.start_time)))
    
    def test_scrape(self):
        song = lyricscraper.song.Song('')
        song.artist = 'Watsky'
        song.title = 'Don\'t Be Nice'
        lyrics = self.scapper.scrape(song)
        self.assertTrue(len(lyrics) > 0)

    def test_no_results(self):
        lyrics = self.scapper.scrape(lyricscraper.song.Song('Oliver Tree - 2002'))
        self.assertTrue(len(lyrics) == 0)
    
        
        
if __name__ == '__main__':
    unittest.main()