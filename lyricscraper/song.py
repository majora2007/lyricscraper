from mutagen.easyid3 import EasyID3
from mutagen.apev2 import APEv2
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, SYLT, USLT, Encoding
from mutagen import File
from .parser import parse_title, parse_artist
import logging
import os

logger = logging.getLogger('lyricscraper')

SYNCED_LYRICS = 'SYLT'
UNSYNCED_LYRICS = 'USLT'

# https://picard-docs.musicbrainz.org/en/technical/tag_mapping.html

class Song():
    artist = ''
    title = ''
    filename = ''
    lyrics = ''
    
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        
        # Extract artist/title from IDv3 tags, fallback to manual name based parsing
        logger.debug('Parsing: {}'.format(self.filename))
        
        try:
            self._parse_artist_from_tags()
            self._parse_title_from_tags()
        except:
            logger.debug('[Song] Could not extact IDv3 tags. Falling back to filename parsing.')
            self.title = parse_title(self.filename)
            self.artist = parse_artist(self.filename)
        
        logger.debug('Extracted: {} - {}'.format(self.artist, self.title))
    
    def _parse_artist_from_tags(self):
        file = File(self.filename)
        for tag in ('TPE1', u'©ART', 'Author', 'Artist', 'artist', 'ARTIST', 'TRACK ARTIST', 'TRACKARTIST', 'TrackArtist', 'Track Artist'):
            try:
                self.artist = file[tag][0]
                break
            except KeyError:
                pass
            except ValueError:
                pass
        
        if self.artist == '':
            self._parse_album_artist_from_tags()
    
    def _parse_album_artist_from_tags(self):
        file = File(self.filename)
        for tag in ('TPE2', 'ALBUMARTIST', u'aART', 'WM/AlbumArtist', 'Album Artist', 'albumartist'):
            try:
                self.artist = file[tag][0]
                break
            except KeyError:
                pass
            except ValueError:
                pass

    def _parse_title_from_tags(self):
        file = File(self.filename)
        for tag in ('TIT2', u'©nam', 'Title', 'title', 'TITLE'):
            try:
                self.title = file[tag][0]
                break
            except KeyError:
                pass
            except ValueError:
                pass
     
    
    def write_lyrics(self, lyrics):
        self.lyrics = lyrics
        tag = ID3(self.filename, v2_version=3)
        tag.add(USLT(encoding=Encoding.UTF8, lang='eng', text=lyrics))
        #tag.setall(UNSYNCED_LYRICS, [SYLT(encoding=Encoding.UTF8, lang='eng', text=lyrics)]) #  format=2, type=1 for SYLT lyrics.
        tag.save(v2_version=3)
        
    

    