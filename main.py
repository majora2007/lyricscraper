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

def print_post_play_info(artist_matches):
    successful_index = 0
    failed_index = 1
    skipped_index = 2
    max_characters_per_line = 68
    template_length = 27
    
    print('\nPost Run Information:')
    if len(artist_matches) == 0:
        print('\tNo artists found')
        return
    
    for artist in artist_matches:
        match = artist_matches[artist]
        #num_of_dots = max_characters_per_line - len(artist) - template_length - len(str(match[successful_index])) - len(str(match[failed_index]))  - len(str(match[skipped_index])) 
        #dots = ''.join(['_' * num_of_dots * 2])
        print('\t{}\t\t{} Success, {} Failed, {} Skipped'.format(artist, match[successful_index], match[failed_index], match[skipped_index]))
    
    successful_sum = sum([item[successful_index] for item in artist_matches.values()])
    failed_sum = sum([item[failed_index] for item in artist_matches.values()])
    skipped_sum = sum([item[skipped_index] for item in artist_matches.values()])
                         
    print('Total: {} Success, {} Failed, {} Skipped'.format(successful_sum, failed_sum, skipped_sum))
    

def scan_dir(root_dir, scrapers, force_overwrite, embed_lyrics):
    artist_matches = {} # Stores a list of [successful, failed, skipped]
    successful_index = 0
    failed_index = 1
    skipped_index = 2
    
    logger.info('Scanning {} for songs...'.format(root_dir))
    for dirpath, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            if parser.is_song(file):
                full_filepath = os.path.join(dirpath, file)
                
                song = Song(full_filepath)
                
                if song.artist not in artist_matches:
                    artist_matches[song.artist] = [0, 0, 0]
                    
                if parser.has_lyrics(full_filepath) and not force_overwrite:
                    logger.debug('Skipping {}, has existing lyric file'.format(file))
                    artist_matches[song.artist][skipped_index] += 1
                    continue
                
                logger.info('Scraping: {} - {}'.format(song.artist, song.title))
                lyrics = ''
                for scraper in scrapers:
                    lyrics = scraper.scrape(song)
                    
                    if len(lyrics) > 0:
                        artist_matches[song.artist][failed_index] += 1
                        break
                
                # Write lyrics to file
                # TODO: Should I move this all into write_lyrics method?
                if len(lyrics) > 0:
                    if embed_lyrics:
                        song.write_lyrics(lyrics, force_overwrite)

                    with codecs.open(os.path.join(dirpath, parser.clean_file_extension(file) + '.txt'), 'w+', 'utf-8') as file:
                        file.write(lyrics.strip())
                    logger.info('\tSuccess: Lyrics written')
                    artist_matches[song.artist][successful_index] += 1
    
    # Print information about the run
    print_post_play_info(artist_matches)
    
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

