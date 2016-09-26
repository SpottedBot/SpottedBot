# functions to get information from the provided target

import requests


# from a given target facebook profile url, get the UID
def uid(url):
    r = requests.post('http://findmyfbid.com/', data={'url': url})
    if r.url.split('/')[3] == 'success':
        return r.url.split('/')[4]
    return ''

# if needed, add other target functions below (like name, relation, registered, etc)
