from lyricscraper.scrapers import ScraperFactory
from lyricscraper import Song
from lyricscraper import parser

import logging
import os
import sys
import codecs

logger = logging.getLogger('lyricscraper')
root_dir = os.getcwd()

scraper_list = ['MusixMatch'] # 'AZLyrics'


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
    

def scan_dir(root_dir, scrapers):
    logger.info('Scanning {} for songs...'.format(root_dir))
    for dirpath, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            if parser.is_song(file):
                song = Song(os.path.join(dirpath, file))
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
    setup_logger(True)
    
    scrapers = setup_scrapers()
    
    directory = ''
    scan_dir(directory, scrapers)
