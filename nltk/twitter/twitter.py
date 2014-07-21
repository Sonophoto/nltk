# Natural Language Toolkit: Twitter client
#
# Copyright (C) 2001-2014 NLTK Project
# Author: Ewan Klein <ewan@inf.ed.ac.uk>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

from functools import partial
import json
import time

from twython import Twython, TwythonStreamer
from util import credentials

class Streamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        self.handler = None
        super().__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        
    def register(self, handler):
        self.handler = handler
        
    def on_success(self, data):
        if 'text' in data:
            self.handler(data)            
            
                  
    def on_error(self, status_code, data):
        print(status_code)


class RESTClient:
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        self.client = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
        
        
    def hydrate(self, infile):
        ids = []
        with open(infile) as f:
            for line in f:
                ids.append(line.rstrip())
                # returns a json object per line 
            return self.client.post('statuses/lookup', {'id':  ids})
                
        
class TweetHandler:
    def __init__(self, client, limit=10, repeat=False, fprefix='tweets'):
        self.client = client
        self.limit = limit
        self.repeat = repeat
        self.counter = 0
        self.fprefix = fprefix
        self.fname = '{0}.{1}.json'.format(fprefix, time.strftime('%Y%m%d-%H%M%S'))
        #self.fname = fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output  = open(self.fname, 'w')
        
    def render(self, data, encoding=None):
        text = data['text']
        if encoding is None:
            try:
                print(text)
            except UnicodeDecodeError:
                print(text.encode(encoding))
        else:
            print(text.encode(encoding))
        self.counter += 1
        if self.counter >= self.limit:
            client.disconnect()

        
    def dump(self, data, verbose=True):
        json_data = json.dumps(data)
        self.output.write(json_data + "\n")
        
        self.counter += 1
        if verbose:
            print('Writing to %s' % self.fname)            
            print(self.counter)
            
        if self.counter >= self.limit:
            self.output.close()
            if not self.repeat:
                client.disconnect()
            else:
                self.output  = open(self.fname, 'w')
                #self.output = open('../streaming_data/' + self.fprefix + '.' 
                               #+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
                  

def dehydrate(infile):
    with open(infile) as tweets:
        ids = [json.loads(t)['id_str'] for t in tweets]        
        return ids


def stream_demo():
    client = Streamer(*credentials('creds.json'))
        
    handler = TweetHandler(client)
    
    method = handler.dump
    method = handler.render      
    client.register(method)
    client.statuses.sample()
    
    
def dehydrate_demo(outfile):
    infile = 'streamer.20140721-105157.json'
    ids = dehydrate(infile)
    with open(outfile, 'w') as f:
        for id_str in ids:
            print(id_str, file=f)
            

def hydrate_demo(infile):
    client = RESTClient(*credentials('creds.json'))
    ids = client.hydrate(infile)
    for i in ids:
        print(i)
        
    
demo = 3

if __name__ == "__main__":
    if demo == 1:
        stream_demo()
    elif demo == 2:
        dehydrate_demo('ids.txt')
    elif demo == 3:
        hydrate_demo('ids.txt')


    
 

    

        