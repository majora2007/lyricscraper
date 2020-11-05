from lyricscraper.scrapers import ScraperFactory
from lyricscraper import Song
from lyricscraper import parser


import argparse
import codecs
import logging
import os
import sys
import random

from gooey import Gooey, GooeyParser


logger = logging.getLogger('lyricscraper')
root_dir = os.getcwd()

scraper_list = ['MusixMatch', 'AZLyrics', 'SongLyrics'] # Genius
def init_args():
    parser = GooeyParser(description='Lyric Scraper')
    
    # Required Parameters
    parser.add_argument('--scan_dir', required=True, metavar='Scan Directory', help='Path to the directory to scan for music. Scans recursively', widget='DirChooser')

    # Optional Parameters
    optional_group = parser.add_argument_group(
        'Optional Options', 
    )
    optional_group.add_argument('--embed', required=False, metavar='Write IDv3 Tags', action='store_true',
                        help='Write any scraped lyrics to IDv3 tags')
    optional_group.add_argument('--force', required=False, metavar='Force Overwrite', action='store_true',
                        help='Forces program to overwrite existing txt (lyric) files')
    optional_group.add_argument('--debug', required=False, metavar='Enable Debug mode', action='store_true', help='Change logging level to debug')
    
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

def random_scraper():
    return random.choice(scraper_list)

def scan_dir(root_dir, scrapers, force_overwrite, embed_lyrics):
    logger.info('Scanning {} for songs...'.format(root_dir))
    for dirpath, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            if parser.is_song(file):
                full_filepath = os.path.join(dirpath, file)
                
                if parser.has_lyrics(full_filepath) and not force_overwrite:
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
                    if embed_lyrics:
                        song.write_lyrics(lyrics, force_overwrite)

                    with codecs.open(os.path.join(dirpath, parser.clean_file_extension(file) + '.txt'), 'w+', 'utf-8') as file:
                        file.write(lyrics.strip())
@Gooey
def main(program_name='Test Readiness Updater', program_description='This program automates updating test readiness status from iTrack'):
    args = init_args()
    setup_logger(bool(args.debug))
    directory = args.scan_dir
    force_overwrite = bool(args.force)
    embed_lyrics = bool(args.embed)
    scrapers = setup_scrapers()
    
    scan_dir(directory, scrapers, force_overwrite, embed_lyrics)

if __name__ == '__main__':
    main()
