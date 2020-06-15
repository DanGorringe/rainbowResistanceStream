from mastodon import Mastodon
from consumer import *
from pprint import pprint
from draw import *
from config import *

def ConvertMtoT(m):
    t = {}
    t['id'] = m['id']
    t['user'] = {}
    t['user']['screen_name'] = m['account']['display_name']
    t['user']['name'] = m['account']['username'] # not 100% this is right
    t['created_at'] = str(m['created_at'])
    t['retweet_count'] = m['reblogs_count']
    t['favorited'] = m['favourited']
    t['favorite_count'] = m['favourites_count']
    t['source'] = '<>Mastodon<>'
    t['text'] = m['content']
    t['entities'] = {}
    t['entities']['media'] = []
    for m in m['media_attachments']:
        t['entities']['media'].append({'media_url':m['remote_url']})
    return t
