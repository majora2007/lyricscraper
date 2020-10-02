import time

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(2)  # 2 per second at most
def PrintNumber(num):
    print(num)
    

""" rate = 5.0 # unit: messages
per  = 8.0 # unit: seconds
allowance = rate # unit: messages
last_check = now() # floating-point, e.g. usec accuracy. Unit: seconds

when (message_received):
  current = now()
  time_passed = current - last_check
  last_check = current
  allowance += time_passed * (rate / per)
  if (allowance > rate):
    allowance = rate # throttle
  if (allowance < 1.0):
    discard_message()
  else:
    forward_message()
    allowance -= 1.0

if __name__ == "__main__":
    print("This should print 1,2,3... at about 2 per second.")
    for i in range(1,100):
        PrintNumber(i)
         """
""" 
from mutagen.easyid3 import EasyID3
audio = EasyID3('C:/Users/Joe/Desktop/Oliver Tree/Ugly is Beautiful (2020)/01. Me, Myself & I.mp3')
print(audio)
title = audio['title'][0]
artist = (audio['artist'] or audio['albumartist'])[0]

print('Extracted: {} - {}'.format(artist, title)) """


file = 'C:\\Users\\Joe\\Documents\\Projects\\Python\\lyricscrapper\\tests\\songs\\01 Hit Parade.flac'
from mutagen.easyid3 import EasyID3
from mutagen.apev2 import APEv2
from mutagen.id3 import ID3, SYLT, USLT, Encoding
from mutagen.oggvorbis import OggVorbis
from mutagen import File
from mutagen.flac import FLAC

""" audio = EasyID3(file)
print(audio) """

#ogg = OggVorbis(file)
#print(ogg.get('TITLE'))
m = File(file)

if isinstance(m, FLAC):
    print('this is a flac file')
print(m)


for tag in ('TPE1', 'TPE2', u'©ART', 'Author', 'Artist', 'artist', 'ARTIST', 'TRACK ARTIST', 'TRACKARTIST', 'TrackArtist', 'Track Artist'):
    try:
        artist = m[tag][0]
        break
    except KeyError:
        pass
    except ValueError:
        pass



exit()


# Update webdriver code
chrome_url = 'https://chromedriver.storage.googleapis.com/index.html' # Needs JS, out of question

import requests
from bs4 import BeautifulSoup
import wget
import os
import zipfile
import shutil
from selenium import webdriver
import stat

def handleError(func, path, exc_info):
    print('Handling Error for file ' , path)
    print(exc_info)
    os.chmod(path, stat.S_IWUSR)
    # Check if file access issue
    if not os.access(path, os.W_OK):
       # Try to change the permision of file
       os.chmod(path, stat.S_IWUSR)
       # call the calling function again
       func(path)

def cleanup():
    # Clear any temp directories created. Should be temp-XX.X.XXXX.XX
    for dirpath, folders, files in os.walk('./', topdown=True):
            for folder in folders:
                if folder.startswith('temp-'):
                    shutil.rmtree(folder, onerror=handleError)


cleanup()

response = requests.get('https://chromedriver.chromium.org/downloads')
soup = BeautifulSoup(response.text, 'html.parser')

versions = []
direct_download_url = 'https://chromedriver.storage.googleapis.com/%s/'
platform = 'win' # win32, mac64, linux64


opts = webdriver.ChromeOptions()
opts.add_argument('--no-sandbox')
opts.add_argument("--disable-gpu")
opts.add_argument('log-level=3')
opts.add_argument("--window-size=1920,1200")
opts.add_argument("--ignore-certificate-errors")
opts.add_argument("--headless")

anchors = soup.find_all('a', {'style': 'background-color:transparent'})
for anchor in anchors:
    if anchor.text.startswith('ChromeDriver '):
        versions.append(anchor.text.replace('ChromeDriver ', ''))

valid_version = ''
file_ext = ''
for version in versions:
    print('Checking against {}'.format(version))
    if platform == 'win':
        file_ext = '.exe'
        url = (direct_download_url % version) + 'chromedriver_win32.zip'
    elif platform == 'mac':
        url = (direct_download_url % version) + 'chromedriver_mac64.zip'
    else:
        url = (direct_download_url % version) + 'chromedriver_linux64.zip'
    
    # Create temp directory
    temp_dir = os.path.abspath('./temp-%s/' % version)
    print('temp dir: ', temp_dir)
    
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    

    filename = wget.download(url, out=temp_dir)
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    full_filename = os.path.join(temp_dir, 'chromedriver' + file_ext)
    print(full_filename)
    driver = None
    try:
        driver = webdriver.Chrome(full_filename, chrome_options=opts)
        driver.get('https://github.com/')
        driver.quit()
    except:
        print('\tFailed')
        if driver is not None:
            driver.quit()
        continue
    
    valid_version = version
    break
    
print('Correct version: {}'.format(valid_version))

if len(valid_version) > 0:
    # Copy from folder, to root directory, cleanup
    temp_dir = os.path.abspath('./temp-%s/' % valid_version)
    full_filename = os.path.join(temp_dir, 'chromedriver' + file_ext)
    shutil.copyfile(full_filename, os.path.join('./', 'chromedriver' + file_ext))
    cleanup()
    