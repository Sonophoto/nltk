
from twython import Twython, TwythonStreamer
from util import credentials

class Streamer(TwythonStreamer):
    #def __init__(self, encoding=None):
        
    def on_success(self, data, encoding=None):
        if 'text' in data:
#            print(data['text'].encode('utf-8'))
            if encoding==None:
                print(data['text'])
            else:
                print(data['text'].encode(encoding))
                  
    def on_error(self, status_code, data):
        print(status_code)


class TwitterRetrieval:
    def __init__(self, cred_fn='creds.json', encoding=None):
        self.creds = credentials(cred_fn=cred_fn)
        self.stream = Streamer(*self.creds)

        
    
    def sample(self):        
        self.stream.statuses.sample()
        
        

if __name__ == "__main__":
    tr = TwitterRetrieval()
    tr.sample()
        