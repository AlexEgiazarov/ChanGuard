import requests
import json
from pprint import pprint
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re
import lxml.html
import url_marker
import csv


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
    if len(urls)>0:
        return urls
    else:
        return None

def handle_com(com):
    com = re.sub('<br><br>', '\n', com)
    com = re.sub('<br>', '\n', com)
    com = re.sub('<span class="quote">&gt;', '>', com)
    com = re.sub('</span>', '\n', com)
    com = re.sub('<wbr>', '', com)
    com = re.sub('&#039;', "'", com)
    com = re.sub('&quot;', '"', com)
    com = re.sub(r'<a.+?</a>', '[REPLY]', com)
    return com


now = dt.now()

#UGLY SUBJECT TO CHANGE
date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'_'+str(now.hour)+'-'+str(now.minute)
with open('dataset/pol_'+date+'.csv', mode='w') as csv_file:

    fieldnames = ['thread_num', 'post_time', 'id', 'country', 'com', 'filename', 'url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

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
        com = handle_com(get_threads('com'))
        
        #post name
        name = get_threads('name')

        #tripcode
        trip = get_threads('trip')

        #id
        ids = get_threads('id')

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

        #country
        country = get_threads('country_name')

        writer.writerow({'thread_num': no, 'post_time': time, 'id': ids, 'country': country, 'com': com, 'filename': filename, 'url': url})

        if 'last_replies' in threads:
            for comment in threads['last_replies']:

                com = handle_com(comment.get('com', 'NaN'))

                ids = comment.get('id', 'NaN')
                
                country = comment.get('country_name', 'NaN')

                time = comment.get('time', 'NaN')

                filename_com = comment.get('filename', 'NaN') + comment.get('ext', 'NaN')
                
                url = find_urls(com)
                
                writer.writerow({'thread_num': no, 'post_time': time, 'id': ids, 'country': country, 'com': com, 'filename': filename, 'url': url})

print("Done saving")