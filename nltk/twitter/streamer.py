from twython import TwythonStreamer
from util import credentials
import json, time

class Streamer(TwythonStreamer):
    """Some code borrowed from
    http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
    """
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, limit=100, repeat=False, fprefix='streamer'):
        self.limit = limit
        self.repeat = repeat
        self.counter = 0
        self.fprefix = fprefix
        self.fname = fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output  = open(self.fname, 'w')
        self.delout  = open('delete.txt', 'a')
        super().__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        

        
    def on_success(self, data):
        """Check properties of tweet to decide how to proceed.
        """
        
        if  'text' in data:
            self.on_status(data)           
        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = data['warnings']
            print(warning['message'])
            return false    

    #def collect(self, n=10, filename):
        #count = 0
        #if self.on_success(data):
        
    def on_status(self, data, verbose=True):
        json_data = json.dumps(data)
        self.output.write(json_data + "\n")
        
        self.counter += 1
        if verbose:
            print('Writing to %s' % self.fname)            
            print(self.counter)
            
        if self.counter >= self.limit:
            self.output.close()
            if not self.repeat:
                self.disconnect()
            else:
                self.output = open('../streaming_data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code, data):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 


    #def on_error(self, status_code, data):
        #print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()
    
    
users = [('ianbaxter_green','21085228'), ('brtgrn', '1625029752'),
         ('GreenYes2014', '1530835490'), ('InappreciableT','774219451')]

following = ', '.join([user[1] for user in users])

tags = 'greens, edinburgh, twitter'
    
stream = Streamer(*credentials('creds.json'))
#stream.statuses.filter(track=tags, follow=following)

stream.statuses.sample()


    