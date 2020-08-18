import unittest
import os
import time

import lyricscraper.scrapers.azlyrics_scraper
import lyricscraper.song

class TestAZLyricsScraper(unittest.TestCase):
    
    start_time = 0
    end_time = 0
    scapper = lyricscraper.scrapers.azlyrics_scraper.AZLyricsScraper()
    
    def setUp(self):
        self.start_time = time.time()
    
    def tearDown(self):
        self.end_time = time.time()
        print('{} took {} to execute'.format(self.id(), (self.end_time - self.start_time)))
    
    def test_scrape(self):
        lyrics = self.scapper.scrape(lyricscraper.song.Song('The New Pornographers - The Fake Headlines.mp3')) # lyricscraper.song.Song('The New Pornographers', 'The Fake Headlines')
        self.assertTrue(len(lyrics) > 0)
        
        lyrics = self.scapper.scrape(lyricscraper.song.Song('Oliver Tree - 1993')) # 'Oliver Tree', '1993'
        self.assertTrue(len(lyrics) > 0)
    
    def test_no_results(self):
        lyrics = self.scapper.scrape(lyricscraper.song.Song('Oliver Tree - 2002'))
        self.assertTrue(len(lyrics) == 0)
    
        
        
if __name__ == '__main__':
    unittest.main()