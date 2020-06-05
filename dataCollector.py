import requests
import json
from pprint import pprint
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re
import lxml.html

import url_marker


#create a request
r = requests.get('https://a.4cdn.org/pol/catalog.json')
r = r.json()

#pprint(r)
#for items in r:
    #for thread in items['threads']:
        #print(thread.keys())

def gen_chan():
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            yield thread

def get_threads(key: str, default='NaN'):
    return threads.get(key, default)

def find_urls(com):
    urls = re.findall(url_marker.WEB_URL_REGEX, com)
    return urls

def handle_com(com):
    com = re.sub('<br><br>', '\n', com)
    com = re.sub('<br>', '\n', com)
    com = re.sub('<span class="quote">&gt;', '>', com)
    com = re.sub('</span>', '\n', com)
    com = re.sub('<wbr>', '', com)
    com = re.sub('&#039;', "'", com)
    com = re.sub('&quot;', '"', com)
    return com

for threads in gen_chan():

    #thread
    no = get_threads('no')

    #now
    now = get_threads('now')
    
    #post time
    time = get_threads('time')

    #my time 
    my_time = dt.today()

    #post text
    #com = BeautifulSoup(get_threads('com')).getText()
    #com = handle_com(BeautifulSoup(get_threads('com')).getText())
    #com = BeautifulSoup(get_threads('com'), 'lxml').getText()
    com = handle_com(get_threads('com'))
    

    #post name
    name = get_threads('name')

    #tripcode
    trip = get_threads('trip')

    #id
    ids = get_threads('ids')

    #capcode?
    capcode = get_threads('capcode')

    #filename 
    filename = get_threads('filename')

    #resto
    rest = get_threads('resto')
    
    #semantic_url
    semantic_url = get_threads('semantic_url')

    #replies
    replies = get_threads('replies')

    #images
    images = get_threads('images')

    #url - need to remake this one probably
    url = find_urls(com)


    print("Thread : ", no)
    print("TripCode : ", trip)
    print("Capcode: ", capcode)
    print(com)
    print(url)
    print('\n')