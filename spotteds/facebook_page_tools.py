import facebook
from django.conf import settings


def page_graph():
    graph = facebook.GraphAPI(settings.FACEBOOK_PAGE_TOKEN)
    return graph
