import requests
import json
from django.conf import settings


def is_safe(url):
    """Is Safe.

    returns true if google and wot safe
    false otherwise
    """
    # Domain white lists
    white_list = [
        'http://i.imgur.com/',
        'https://i.imgur.com/',
    ]

    def is_whitelist(url):
        for domain in white_list:
            if url.startswith(domain):
                return True
        return False

    if is_whitelist(url):
        return True

    if settings.WOT_SECRET and not is_WOT_safe(url):
        return False

    if settings.GSB_SECRET and not is_google_safe(url):
        return False

    return True


def is_WOT_safe(url):
    """WOT API Wrapper.

    calls the api and checks for high levels of safety confidence
    """
    secret = settings.WOT_SECRET
    payload = {'hosts': url, 'key': secret}
    response = requests.get("http://api.mywot.com/0.4/public_link_json2", params=payload)

    if not response.json() and response.status_code == requests.codes.ok:
        return True

    for domain in response.json():
        inside = response.json()[domain]
        try:
            if inside['0'][0] < 60 and inside['0'][1] > 20:
                return False
        except:
            pass
        try:
            if inside['4'][0] < 60 and inside['4'][1] > 20:
                return False
        except:
            pass
        return True


def is_google_safe(url):
    """Google Safe Browsing Wrapper

    calls api, checks all lists and returns true if not found in any list
    false otherwise
    """

    secret = settings.GSB_SECRET
    params = {
        "key": secret
    }
    payload = json.dumps({
        "client": {
            "clientId": 'spottedsystem',
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION", "MALICIOUS_BINARY", "UNWANTED_SOFTWARE", ],
            "platformTypes": ["ANY_PLATFORM", "WINDOWS", "LINUX", "OSX", "ANDROID", "CHROME", "IOS"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url},
            ]
        }
    })

    response = requests.post("https://safebrowsing.googleapis.com/v4/threatMatches:find", params=params, data=payload)

    return not response.json() and response.status_code == requests.codes.ok
