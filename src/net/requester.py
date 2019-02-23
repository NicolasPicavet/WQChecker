import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

WORLD_QUEST_URL = 'https://www.wowhead.com/world-quests/'
QUEST_URL= 'https://www.wowhead.com/quest='

def getQuestUrl(questId):
    return QUEST_URL + str(questId)

def getWorldQuestsHtml(extensions, region, dump=False):
    html = ''
    for e in extensions:
        html += str(_get(WORLD_QUEST_URL + e + '/' + region, dump))
    return html

def getQuestName(questId, dump=False):
    try:
        return next(iter(_get(getQuestUrl(questId), dump).select('h1') or []), None).text
    except AttributeError:
        return '!Quest name not found!'

def _get(url, dump):
    html = BeautifulSoup(_simple_get(url), 'html.parser')
    if dump:
        file = open('dump.html','w+')
        file.write(str(html))
        file.close()
    return html

# from https://realpython.com/python-web-scraping-practical-introduction/

def _simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with requests.get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)