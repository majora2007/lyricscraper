import re
import pathlib

SONG_EXTENSIONS = ('.mp3', '.m4a', '.ogg', '.flac')

TITLE_REGEX = [
    # Track without artist (01. trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}([-| .]{0,1})[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
    # Track with artist (01 - artist - trackName)
    re.compile(r'(?P<trackNumber>\d*){0,1}([-| ]{0,1})(?P<artist>[a-zA-Z0-9, ().&_]*)[-| ]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
    # Track without artist (01 - trackName), Track without trackNumber or artist(trackName), Track without trackNumber and  with artist(artist - trackName)
    re.compile(r'(?P<trackNumber>\d*)[-| .]{0,1}(?P<trackName>[a-zA-Z0-9, ().&_]+)', re.IGNORECASE),
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
        print('Found match on ', i)
        return clean_title(extracted_title)
    return ''

def parse_artist(filename):
    """ Attempts to parse song artist from filename. Will strip out separators at start of string. If no title is found, returns empty string"""
    name = clean_file_extension(filename)
    for regex in TITLE_REGEX:
        m = re.search(regex, name)

        if m is None:
            continue

        extracted_title = m.group('artist')
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