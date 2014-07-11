import os
import json

from twython import Twython
from util import credentials

class Twitter:

    FILE ='tweets.json'

    def authenticate(self, cred_fn):
        creds = credentials(cred_fn=cred_fn)
        self.twitter = Twython(*creds)

    def capture(self, outfn=FILE, output=False):
        tweets = self.twitter.search(q='@GreenYes2014')
        outfile = open(outfn, 'w')
        
        if output:
            print(json.dumps(tweets, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            json.dump(tweets, outfile)
            print('Capturing tweets in %s' % outfn)
                       
            
    def tweet_text(self, fn=FILE, dumptofile=True):
        
        with open(fn) as infile:
            jsono = json.load(infile)
            
        text = (st['text'] for st in jsono['statuses'])
        
        if not dumptofile:
            for t in text: 
                print(t)
        else:
            outfn = os.path.splitext(fn)[0] + '.txt'
            print('Writing to %s' % outfn)
            with open(outfn, 'w') as outfile:
                for t in text:
                    print(t, file=outfile)


tw = Twitter()
tw.authenticate('creds.json')
#tw.capture()
tw.tweet_text(fn='test.json', dumptofile=False)
