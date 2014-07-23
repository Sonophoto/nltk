# Natural Language Toolkit: Twitter client
#
# Copyright (C) 2001-2014 NLTK Project
# Author: Ewan Klein <ewan@inf.ed.ac.uk>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

import json
import os
import datetime

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


class Query:
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        self.client = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
        
        
    def hydrate(self, infile):
        ids = []
        with open(infile) as f:
            for line in f:
                ids.append(line.rstrip())
                id_chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]
                # returns line-delimited json
            return self.client.post('statuses/lookup', {'id':  id_chunks})
                
        
class TweetHandler:
    def __init__(self, client, limit=2000, repeat=False, fprefix='tweets', subdir='streamed_data', ):
        self.client = client
        self.limit = limit
        self.repeat = repeat
        self.counter = 0
        self.subdir = subdir
        self.fprefix = fprefix
        self.fname = self.timestamped_file()
        self.output  = open(self.fname, 'w')
        
    def timestamped_file(self):
        subdir = self.subdir
        fprefix = self.fprefix
        if subdir:
                if not os.path.exists(subdir):
                    os.mkdir(subdir)
                   
        fname = os.path.join(subdir, fprefix)
        fmt = '%Y%m%d-%H%M%S'
        ts = datetime.datetime.now().strftime(fmt)
        outfile = '{0}.{1}.json'.format(fname, ts)
        return outfile    
        
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
        """
        Dump Twitter data as line-delimited JSON into one or more files.
        """
        json_data = json.dumps(data)
        self.output.write(json_data + "\n")        
        self.counter += 1
        if verbose:
            print('Writing to {}'.format(self.fname))           
            
        
        if self.counter >= self.limit:
            self.output.close()
            if not self.repeat:
                self.client.disconnect()
            else:
                self.output = open(self.timestamped_file(), 'w')               
                self.counter = 0
                if verbose:
                    print('Writing to new file {}'.format(self.fname))           
                    #print(self.counter)                    
                  

def dehydrate(infile):
    with open(infile) as tweets:
        ids = [json.loads(t)['id_str'] for t in tweets]        
        return ids


def stream_demo():
    client = Streamer(*credentials('creds.json'))
        
    handler = TweetHandler(client)
    
    method = handler.dump
    #method = handler.render      
    client.register(method)
    client.statuses.sample()
    
    
def dehydrate_demo(outfile):
    infile = 'streamed_data/tweets.20140723-163436.json'
    ids = dehydrate(infile)
    with open(outfile, 'w') as f:
        for id_str in ids:
            print(id_str, file=f)
            

def hydrate_demo(infile):
    client = Query(*credentials('creds.json'))
    ids = client.hydrate(infile)
    for i in ids:
        print(i)
        
    
demos = [3]

if __name__ == "__main__":
    if 1 in demos:
        stream_demo()
    if 2 in demos:
        dehydrate_demo('ids.txt')
    if 3 in demos:
        hydrate_demo('ids.txt')


    
 

    

        