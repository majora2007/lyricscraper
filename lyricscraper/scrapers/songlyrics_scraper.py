from .scraper import Scraper
from .. import RateLimited

import base64
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("lyricscraper")


class SongLyricsScraper(Scraper):
    """Pulls lyrics from Song Lyrics"""

    QUERY_URL = "http://www.songlyrics.com/index.php?section=search&searchW=%s&submit=Search"  # Query parameters (Oliver+Tree+-+Hurt)

    def __init__(self):
        super().__init__()

    def name(self):
        return "SongLyrics"

    @RateLimited(1)  # Limit at 1 calls per second
    def scrape(self, song):
        query = song.artist + " - " + song.title
        query = query.replace(" ", "+")
        url = self.QUERY_URL % query

        logger.info("\t[SongLyrics] Searching for {}".format(url))

        search_results = requests.get(url, headers=self.request_headers).content
        soup = BeautifulSoup(search_results, "html.parser")

        lyrics = ""

        # Validate results found
        try:
            if soup.find("div", {"class": "alert alert-warning"}) is not None:
                logger.debug("[AZLyrics] No match found")
                return lyrics
        except:
            pass

        if soup.find("table") is None:
            logger.error("[SongLyrics] failed to find table, critical error.")
            logger.debug(search_results)
            return lyrics

        for a in soup.find("table").find_all("a"):
            if (
                a.text is not None and song.title in a.text
            ):  # TODO: We should validate the artist as well
                if a.get("href").startswith("https://www.azlyrics.com/lyrics/"):
                    search_results = requests.get(
                        a.get("href"), headers=self.request_headers
                    ).content
                    lyric_soup = BeautifulSoup(
                        search_results, "html.parser"
                    )  # TODO: Switch out with lxml

                    for div in lyric_soup.find(
                        "div", {"class": "col-xs-12 col-lg-8 text-center"}
                    ).find_all("div"):
                        if div.get("class") is None and div.get("id") is None:
                            lyrics = div.text

        # Clean up lyrics
        return lyrics
