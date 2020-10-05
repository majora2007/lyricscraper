import unittest
import os
import time

import lyricscraper.song

class TestSong(unittest.TestCase):
    
    start_time = 0
    end_time = 0
    
    def setUp(self):
        self.start_time = time.time()
    
    def tearDown(self):
        self.end_time = time.time()
        print('{} took {} to execute'.format(self.id(), (self.end_time - self.start_time)))
    
    def test_write_tags(self):
        song = lyricscraper.Song('./tests/songs/13. Introspective.mp3')
        seed = next(range(1000))
        lyrics = 'Test ' + str(seed)
        
        song.write_lyrics(lyrics, True)
        song.read_lyrics()
        
        self.assertEqual(song.lyrics, lyrics)
        
        
if __name__ == '__main__':
    unittest.main()