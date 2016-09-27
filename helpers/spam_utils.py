# get posts with many ANGRY reactions, sets them as spam and delete from page, until moderation check
# leaving as separate file so we can choose when to execute it(every POST or a scheduled job
# eg. http://stackoverflow.com/questions/573618/django-set-up-a-scheduled-job )

import os

from facebook import GraphAPI

from app.models import Spotted
from helpers.page_utils import delete, re_post

token = os.environ.get('FACEBOOK_PAGE_TOKEN')
page_id = os.environ.get('PAGE_ID')


# get a list of possible spams
def get_spam_list():
    graph = GraphAPI(token)
    obj = page_id + '/feed?fields=reactions.type(ANGRY).limit(0).summary(total_count)&limit=100'
    data = (graph.get_object(obj))
    spam_list = []

    for post in data['data']:
        if post['reactions']['summary']['total_count'] >= 0:
            spam_list.append(post['id'])
    return spam_list


# set the posts in spam_list as spam, calling delete()
def set_spam(spam_list):
    for post in spam_list:
        try:
            obj = Spotted.objects.get(post_id=post)
        except:
            continue
        if obj.spam is False:
            delete(obj.post_id, False)


# execute the above functions in a single call
def clean_spam():
    spam_list = get_spam_list()
    set_spam(spam_list)


# unset a spam post, reposting it
def un_spam(id):
    s = Spotted.objects.get(id=id)
    s.spam = False
    post_id = re_post(s.message, s.attachment)
    s.post_id = post_id
    s.save()
