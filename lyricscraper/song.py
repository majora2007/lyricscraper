from mutagen.easyid3 import EasyID3
from .parser import parse_title, parse_artist
import logging

logger = logging.getLogger('lyricscraper')

class Song():
    artist = ''
    title = ''
    filename = ''
    lyrics = ''
    
    def __init__(self, filename):
        self.filename = filename
        
        # Extract artist/title from IDv3 tags, fallback to manual name based parsing
        try:
            audio = EasyID3(self.filename)
            self.title = audio['title'][0]
            self.artist = (audio['artist'] or audio['albumartist'])[0]
        except:
            logger.debug('[Song] Could not extact IDv3 tags. Falling back to filename parsing.')
            self.title = parse_title(self.filename)
            self.artist = parse_artist(self.filename)
        
        print('Extracted: {} - {}'.format(self.artist, self.title))
    
    
        
        
    
    
        
        
        
    