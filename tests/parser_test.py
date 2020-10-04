import unittest
import os
import time

import lyricscraper.parser

class TestParse(unittest.TestCase):
    
    start_time = 0
    end_time = 0
    
    def setUp(self):
        self.start_time = time.time()
    
    def tearDown(self):
        self.end_time = time.time()
        print('{} took {} to execute'.format(self.id(), (self.end_time - self.start_time)))
    
    def test_parse_title(self):
        self.assertEqual(lyricscraper.parser.parse_title('The Format - Give It Up.mp3'), 'Give It Up')
        self.assertEqual(lyricscraper.parser.parse_title('01. Me, Myself & I.mp3'), 'Me, Myself & I')
        self.assertEqual(lyricscraper.Song('./tests/songs/13. Introspective.mp3').title, 'Introspective')
        
    
    def test_parse_artist(self):
        self.assertEqual(lyricscraper.parser.parse_artist('The Format - Give It Up.mp3'), 'The Format')
        self.assertEqual(lyricscraper.Song('./tests/songs/13. Introspective.mp3').artist, 'Oliver Tree')
        self.assertEqual(lyricscraper.Song('./tests/songs/01 Hit Parade.flac').artist, 'Neon Indian')
    
    def test_is_song(self):
        self.assertTrue(lyricscraper.parser.is_song('The Format - Give It Up.mp3'))
        self.assertTrue(lyricscraper.parser.is_song('The Format - Give It Up.flac'))
        self.assertTrue(lyricscraper.parser.is_song('The Format - Give It Up.m4a'))
        
        self.assertFalse(lyricscraper.parser.is_song('The Format - Give It Up.mp4'))
        self.assertFalse(lyricscraper.parser.is_song('The Format - Give It Up.mpeg4'))
        

        
        
if __name__ == '__main__':
    unittest.main()