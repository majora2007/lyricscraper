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
        song = lyricscraper.song.Song('')
        song.artist = 'The New Pornographers'
        song.title = 'The Fake Headlines'
        lyrics = self.scapper.scrape(song)
        self.assertTrue(len(lyrics) > 0)
        
        song = lyricscraper.song.Song('')
        song.artist = 'Oliver Tree'
        song.title = '1993'
        lyrics = self.scapper.scrape(song) 
        self.assertTrue(len(lyrics) > 0)
        
        song = lyricscraper.song.Song('')
        song.artist = 'Oliver Tree'
        song.title = 'I\'m Gone'
        lyrics = self.scapper.scrape(song) 
        self.assertTrue(len(lyrics) > 0)
    
    def test_no_results(self):
        song = lyricscraper.song.Song('')
        song.artist = 'Oliver Tree'
        song.title = '2002'
        lyrics = self.scapper.scrape(song) 
        self.assertTrue(len(lyrics) == 0)
    
        
        
if __name__ == '__main__':
    unittest.main()