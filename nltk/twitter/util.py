import datetime
import os



"""
Fetch credentials from a JSON format file

>>> creds = credentials('creds.json')
>>> len(creds)
4

"""

import json

def load_creds(cred_fn):
    with open(cred_fn) as infile:
        creds = json.load(infile)  
    return creds


def credentials(cred_fn):
        creds = load_creds(cred_fn)
        APP_KEY = creds['APP_KEY']
        APP_SECRET = creds['APP_SECRET']
        OAUTH_TOKEN = creds['OAUTH_TOKEN']
        OAUTH_TOKEN_SECRET = creds['OAUTH_TOKEN_SECRET']
        
        return (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    

def timestamped_file(fprefix, subdir=''):
    if subdir:
            if not os.path.exists(subdir):
                os.mkdir(subdir)
               
    fname = os.path.join(subdir, fprefix)
    fmt = '%Y%m%d-%H%M%S'
    ts = datetime.datetime.now().strftime(fmt)
    outfile = '{0}.{1}.json'.format(fname, ts)
    return outfile
    
    
    
    