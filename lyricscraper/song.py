from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, SYLT, USLT, Encoding
from .parser import parse_title, parse_artist
import logging

logger = logging.getLogger('lyricscraper')

SYNCED_LYRICS = 'SYLT'
UNSYNCED_LYRICS = 'USLT'

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
        
        logger.debug('Extracted: {} - {}'.format(self.artist, self.title))
    
    def write_lyrics(self, lyrics):
        self.lyrics = lyrics
        tag = ID3(self.filename, v2_version=3)
        tag.add(USLT(encoding=Encoding.UTF8, lang='eng', text=lyrics))
        #tag.setall(UNSYNCED_LYRICS, [SYLT(encoding=Encoding.UTF8, lang='eng', text=lyrics)]) #  format=2, type=1 for SYLT lyrics.
        tag.save(v2_version=3)
        
    
    
        
        
    
    
        
        
        
    