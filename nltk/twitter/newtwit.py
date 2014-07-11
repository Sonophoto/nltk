
from twython import Twython, TwythonStreamer
from util import credentials

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'].encode('utf-8'))

    def on_error(self, status_code, data):
        print(status_code)


class TwitterRetrieval:
    def __init__(self, cred_fn='creds.json'):
        self.creds = credentials(cred_fn=cred_fn)

        
    
    def sample(self):
        stream = MyStreamer(*self.creds)
        stream.statuses.sample()
        
        

if __name__ == "__main__":
    tr = TwitterRetrieval()
    tr.sample()
        