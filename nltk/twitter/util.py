import os



"""
Fetch credentials from a JSON format file

>>> creds = credentials('creds.json')
>>> len(creds)
4

"""



#def load_creds(cred_fn):
    #with open(cred_fn) as infile:
        #creds = json.load(infile)  
    #return creds


#def credentials(cred_fn):
        #creds = load_creds(cred_fn)
        #APP_KEY = creds['APP_KEY']
        #APP_SECRET = creds['APP_SECRET']
        #OAUTH_TOKEN = creds['OAUTH_TOKEN']
        #OAUTH_TOKEN_SECRET = creds['OAUTH_TOKEN_SECRET']
        
        #return (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    

def authenticate(creds_file=None):
    """
    Read OAuth credentials from a text file.  File format:
   
    app_key=YOUR_APP_KEY
    app_secret=YOUR_APP_SECRET
    oauth_token=ACCESS_TOKEN
    oauth_token_secret=ACCESS_TOKEN_SECRET
   
    :param file_name: File containing credentials. None (default) reads
    data from "./credentials.txt"
    """
    if creds_file is None:
        path = os.path.dirname(__file__)
        creds_file = os.path.join(path, 'credentials.txt')

    with open(creds_file) as f:
        oauth = {}
        for line in f:
            if '=' in line:
                name, value = line.split('=', 1)
                oauth[name.strip()] = value.strip()    
    return oauth
    
    
    
    