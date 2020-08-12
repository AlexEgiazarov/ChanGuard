import re
import json
from pprint import pprint
from datetime import datetime as dt
import csv
from bs4 import BeautifulSoup
import lxml.html
import requests
import url_marker
import time


#pprint(r)
#for items in r:
    #for thread in items['threads']:
        #print(thread.keys())

def gen_chan():
    """Function that collectes and yields all the threads on a given board

    Yields:
        dict: thread content in a dictionary format
    """
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            yield thread

def get_threads(key: str, default='NaN'):
    """Function for extracting data given a string key from the thread dictionary

    Args:
        key (str): dict key for extraction
        default (str, optional): Defaults to 'NaN'.

    Returns:
        list: returns comments of the thread
    """
    return threads.get(key, default)

def find_urls(com):
    """Function for extracting urls from the comment

    Args:
        com (str): comment

    Returns:
        str: an extracted url or None if urls were not found
    """
    urls = re.findall(url_marker.WEB_URL_REGEX, com)
    if len(urls)>0:
        return urls
    else:
        return None

def handle_com(com):
    """Ugly function to remove all the html tags from the comment

    Args:
        com (str): comment

    Returns:
        str: stripped from html tags comment
    """
    com = re.sub('<br><br>', '\n', com)
    com = re.sub('<br>', '\n', com)
    com = re.sub('<span class="quote">&gt;', '>', com)
    com = re.sub('</span>', '\n', com)
    com = re.sub('<wbr>', '', com)
    com = re.sub('&#039;', "'", com)
    com = re.sub('&quot;', '"', com)
    com = re.sub(r'<a.+?</a>', '[REPLY]', com)
    return com


def cycle_collector(board_name):
    """Function that takes snapshot of the board and logs data in dataframe

    Args:
        board_name (str): board to log
    """

    #create a request
    r = requests.get(board_name)
    #r = requests.get('https://a.4cdn.org/tv/catalog.json')
    r = r.json()

    #getting a date
    now = dt.now()

    #UGLY SUBJECT TO CHANGE
    date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'_'+str(now.hour)+'-'+str(now.minute)

    #open and save threads into the csv file
    with open('dataset/pol_'+date+'.csv', mode='w') as csv_file:
    #with open('dataset/tv_'+date+'.csv', mode='w') as csv_file:

        #create field names
        fieldnames = ['thread_num', 'post_time', 'id', 'country', 'com', 'filename', 'url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        #for each thread on the board
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

            writer.writerow({'thread_num': no,
                             'post_time': time,
                             'id': ids,
                             'country': country,
                             'com': com,
                             'filename': filename,
                             'url': url})

            #write all thread replies
            if 'last_replies' in threads:
                for comment in threads['last_replies']:

                    #comment
                    com = handle_com(comment.get('com', 'NaN'))
                    #poster id
                    ids = comment.get('id', 'NaN')
                    #poster country
                    country = comment.get('country_name', 'NaN')
                    #post time
                    time = comment.get('time', 'NaN')
                    #filename
                    filename_com = comment.get('filename', 'NaN') + comment.get('ext', 'NaN')
                    #urls if present
                    url = find_urls(com)

                    writer.writerow({'thread_num': no,
                                     'post_time': time,
                                     'id': ids,
                                     'country': country,
                                     'com': com,
                                     'filename': filename,
                                     'url': url})

    print("Done saving ", date)

def main():
    """Main function that runs a logging loop
    """
    board_name = 'https://a.4cdn.org/pol/catalog.json'

    while True:
        cycle_collector(board_name)
        time.sleep(300)

if __name__ == "__main__":
    main()
    