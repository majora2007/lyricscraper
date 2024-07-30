# lyricscraper
The goal of this program is to provide a simple way to scrape lyrics from the web. Just point it to a directory and let it rip. By default, it 
downloads txt files next to the song files. You can have it also write to IDv3 tags for lyrics. This isn't supported by all media 
players, but nice to have. 


## Note
This program was only tested and built for Windows, but should work on linux if built that way ()

## Nix
if you have [Nix](https://nixos.org) installed you can simply run
```bash
nix run github:majora2007/lyricscraper
```


# TODO
- Ensure force overwrite respects embeded lyrics as well and update documentation on GUI. 
- Clean up how logging works to GUI to be cleaner, but also preserve errors.
- Clear log on pressing edit/restart

# Add Scrapers:
- genius.com
- songlyrics.com
- www.lyricsbox.com
- www.elyrics.net
- www.karaoke-lyrics.net

# BUG:

- MusixMatch is not pulling lyrics from the web.