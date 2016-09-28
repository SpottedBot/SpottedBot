# Utils to post and delete messages from timeline

from facebook import GraphAPI
import os
from app.models import Spotted

graph = GraphAPI(os.environ.get('FACEBOOK_PAGE_TOKEN'))


# escape text, get next id, edit message, push message to page and create entry on DB
def post(message, author, target, attachment):
    # escape text

    try:
        new_id = Spotted.objects.all().order_by("-id")[0].id + 1
    except (IndexError):
        new_id = 1
    f_message = "#" + str(new_id) + "\n\n" + message
    resp = graph.put_wall_post(f_message, {'link': attachment})
    s = Spotted(message=message, author=author, target=target, attachment=attachment, post_id=resp['id'])
    s.save()

    return s


# takes the id(Spotted ID, shown on post) and db_remove(if true, remove from DB as well) and does what it is supposed
# to do, setting the entry as spam if db_remove == False
def delete(id, db_remove):
    p = Spotted.objects.get(id=id)
    try:
        graph.delete_object(p.post_id)
    except:
        pass
    if db_remove:
        p.delete()
        return
    p.spam = True
    p.save()
    return


# re post a Spotted and return its new post_id
def re_post(message, attachment, id):
    f_message = "#" + str(id) + "\n\n" + message
    resp = graph.put_wall_post(f_message, {'link': attachment})
    return resp['id']
