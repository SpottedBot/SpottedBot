import os

import mechanicalsoup
import requests


def global_id(url):
    r = requests.post('http://findmyfbid.com/', data={'url': url})
    if r.url.split('/')[3] == 'success':
        return r.url.split('/')[4]
    return ''


def profile_from_scope(scope_id):
    scope_url = "https://www.facebook.com/app_scoped_user_id/" + str(scope_id)
    browser = mechanicalsoup.Browser()

    login_page = browser.get("https://www.facebook.com/")

    login_form = login_page.soup.select("#login_form")[0]

    login_form.select("#email")[0]['value'] = os.environ.get('FACEBOOK_USER_EMAIL')
    login_form.select("#pass")[0]['value'] = os.environ.get('FACEBOOK_USER_PASS')

    browser.submit(login_form, login_page.url)

    page = browser.get(scope_url)
    return page.url
