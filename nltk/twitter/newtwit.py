
from functools import partial
import json
import time

from twython import Twython, TwythonStreamer
from util import credentials

class Streamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, handler):
        self.handler = handler
        super().__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        
    def on_success(self, data):
        if 'text' in data:
            self.handler(data)
            if self.handler(data) == False:
                self.disconnect()
            
            
                  
    def on_error(self, status_code, data):
        print(status_code)


        
def tweet_print(data, encoding=None):
    text = data['text']
    if encoding is None:
        print(text)
    else:
        print(text.encode(encoding))
    return True
        
class TweetStorage:
    def __init__(self, limit=10, repeat=False, fprefix='streamer'):
        self.limit = limit
        self.repeat = repeat
        self.counter = 0
        self.fprefix = fprefix
        self.fname = '{0}.{1}.json'.format(fprefix, time.strftime('%Y%m%d-%H%M%S'))
        #self.fname = fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output  = open(self.fname, 'w')
        
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
                return False
            else:
                self.output  = open(self.fname, 'w')
                #self.output = open('../streaming_data/' + self.fprefix + '.' 
                               #+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
            return True        
          

if __name__ == "__main__":
 
    print_h = partial(tweet_print, encoding='utf8')
    store = TweetStorage()
    store_h = store.dump
    
    stream = Streamer(*credentials('creds.json'), handler=store_h)
    stream.statuses.sample()
    
    #tr = TwitterRetrieval()
    #tr.sample()

        