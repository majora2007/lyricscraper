import os
import re
import pathlib

SONG_EXTENSIONS = ('.mp3', '.m4a', '.ogg', '.flac')

TITLE_REGEX = [
    # artist - title
    re.compile(r'.*-(?P<trackName>.*)', re.IGNORECASE),
    # Track without artist (01. trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}([-| .]{0,1})[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)(?P<artist>)', re.IGNORECASE),
    # Track with artist (01 - artist - trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}([-| ]{0,1})?(?P<artist>[a-zA-Z0-9, ().&_]*)[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
    # Track without artist (01 - trackName), Track without trackNumber or artist(trackName), Track without trackNumber and  with artist(artist - trackName)
    re.compile(r'(?P<trackNumber>\d*)[-| .]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)(?P<artist>)', re.IGNORECASE),
    # Track with artist and starting title (01 - artist - trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}[-| ]{0,1}(?P<artist>[a-zA-Z0-9, ().&_]*)[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
    
    # Custom 01. title
    re.compile(r'\d{1,3}\.? (?P<trackName>.*)', re.IGNORECASE),
    
]

ARTIST_REGEX = [
    # artist - title
    re.compile(r'(?P<artist>.*)-(?P<trackName>.*)', re.IGNORECASE),
    # Track with artist (01 - artist - trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}([-| ]{0,1})?(?P<artist>[a-zA-Z0-9, ().&_]*)[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
    # Track with artist and starting title (01 - artist - trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}[-| ]{0,1}(?P<artist>[a-zA-Z0-9, ().&_]*)[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE), 
]

def parse_title(filename):
    """ Attempts to parse song title from filename. Will strip out separators at start of string. If no title is found, returns empty string"""
    name = clean_file_extension(filename)
    i = -1
    for regex in TITLE_REGEX:
        m = re.search(regex, name)
        i += 1
        if m is None:
            continue

        extracted_title = m.group('trackName')
        print('Matched on ' + str(i))
        return clean_title(extracted_title)
    return ''

def parse_artist(filename):
    """ Attempts to parse song artist from filename. Will strip out separators at start of string. If no title is found, returns empty string"""
    name = clean_file_extension(filename)
    i = -1
    for regex in ARTIST_REGEX:
        m = re.search(regex, name)
        i += 1
        if m is None:
            continue

        extracted_title = m.group('artist')
        print('Matched on ' + str(i))
        return clean_title(extracted_title)
    return ''

def is_song(file):
    """ Returns true if file is a known song extension. This list is self-maintained. """
    return file.lower().endswith(SONG_EXTENSIONS)

def get_file_extension(file):
    return pathlib.Path(file).suffix

def clean_title(title):
    return title.strip()

def clean_file_extension(filename):
    """ Returns just the filename """
    return pathlib.Path(filename).stem

def has_lyrics(full_song_file):
    no_extension_file = get_file_extension(full_song_file)
    return os.path.exists(full_song_file.replace(no_extension_file, '.txt')) or os.path.exists(full_song_file.replace(no_extension_file, '.lrc'))