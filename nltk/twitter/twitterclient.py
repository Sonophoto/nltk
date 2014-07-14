from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager



class TwitterRetrieval(object):
    def __init__(self, credentials='credentials.txt'):
        o = TwitterOAuth.read_file(credentials)
        self.api = TwitterAPI(
            o.consumer_key,
            o.consumer_secret,
            o.access_token_key,
            o.access_token_secret)
        
    def search(self, query):
        try:
            pager = TwitterRestPager(self.api, 'search/tweets', {'q': query})
            for item in pager.get_iterator():
                print(item['text'] if 'text' in item else item)
        
        except Exception as e:
            print(e)
            
    def sample(self):
       
        r = self.api.request('statuses/sample')
        for item in r.get_iterator():
            if 'text' in item:
                print(item['id'], item['text'])
        

            
    def filter(self, track_term):
        try:   
            self.api.request('statuses/filter', {'track': track_term})
            for item in r.get_iterator():
                print(item['text'] if 'text' in item else item)
        
        except Exception as e:
            print(e)    
        
    def statusID(self, tweet_id):
        try:
            r = self.api.request('statuses/show/:PARAM', {'id': tweet_id})
           
            for item in r.get_iterator():
                print(item['text'].encode('utf-8') if 'text' in item else item)
        
        except Exception as e:
            print(e)        

    
    
if __name__ == "__main__":
    retriever = TwitterRetrieval()
    #retriever.sample()
    retriever.statusID(487276326278410241)