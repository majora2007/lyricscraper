from lyricscraper.scrapers import ScraperFactory
from lyricscraper import Song
from lyricscraper import parser

import argparse
import codecs
import logging
import os
import sys


logger = logging.getLogger('lyricscraper')
root_dir = os.getcwd()

scraper_list = ['MusixMatch'] # 'AZLyrics'

def init_args():
    parser = argparse.ArgumentParser()
    # Required Parameters
    parser.add_argument('--scan_dir', required=False, nargs=1, help="Path to the directory to scan for music. Scans recursively")

    # Optional Parameters
    parser.add_argument('--force', required=False, action='store_true',
                        help="Forces program to overwrite existing txt files")
    parser.add_argument('--debug', required=False, action='store_true', help="Change logging level to debug")
    return parser.parse_args()


def get_argument(argument, default=None):
    if argument:
        return argument[0]
    else:
        return default

def setup_logger(debug):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler('lyricscraper.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    
    if debug:
        logger.setLevel(logging.DEBUG)

def setup_scrapers():
    scrapers = []
    for name in scraper_list:
        scrapers.append(ScraperFactory().get_scraper(name))
    
    return scrapers

def has_lyrics(full_song_file):
    no_extension_file = parser.get_file_extension(full_song_file)
    return os.path.exists(full_song_file.replace(no_extension_file, '.txt')) or os.path.exists(full_song_file.replace(no_extension_file, '.lrc'))

def scan_dir(root_dir, scrapers, force_overwrite):
    logger.info('Scanning {} for songs...'.format(root_dir))
    for dirpath, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            if parser.is_song(file):
                full_filepath = os.path.join(dirpath, file)
                
                if has_lyrics(full_filepath) and not force_overwrite:
                    print('Skipping {}, has existing lyric file', file)
                    continue
                
                song = Song(full_filepath)
                
                lyrics = ''
                for scraper in scrapers:
                    lyrics = scraper.scrape(song)
                    
                    if len(lyrics) > 0:
                        break
                
                # Write lyrics to file
                if len(lyrics) > 0:
                    with codecs.open(os.path.join(dirpath, parser.clean_file_extension(file) + '.txt'), 'w+', 'utf-8') as file:
                        file.write(lyrics.strip())

if __name__ == '__main__':
    
    args = init_args()
    setup_logger(bool(args.debug))
    directory = get_argument(args.scan_dir)
    force_overwrite = bool(args.force)
    scrapers = setup_scrapers()
    
    scan_dir(directory, scrapers, force_overwrite)
