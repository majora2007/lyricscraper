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

