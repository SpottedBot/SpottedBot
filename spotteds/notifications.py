from custom_auth.facebook_methods import get_graph as app_graph
from django.shortcuts import reverse
from project.manual_error_report import no_request_exception
import traceback
from facebook import GraphAPIError
from celery import shared_task


@shared_task
def author_notification(instance_id):
    """Author Notification.

    render and send author notifications
    """
    from .models import Spotted
    instance = Spotted.objects.get(id=instance_id)
    template = "Um de seus Spotteds acaba de ser postado!"
    href = reverse('spotteds:view_spotted', kwargs={'spottedid': instance.spotted_count})
    userid = instance.author.facebookuser.social_id

    try:
        app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)
    except GraphAPIError as e:
        if 'Only web canvas apps can send app notifications' in getattr(e, 'message', ''):
            print(e.message.replace('\n', '\\n').replace('\r', '\\r')[:989])
        else:
            tb = traceback.format_exc()
            no_request_exception(tb, e)


@shared_task
def target_notification(instance_id):
    """Target Notification.

    render and send target notifications
    """
    from .models import Spotted
    instance = Spotted.objects.get(id=instance_id)
    if instance.author and instance.share_with_crush:
        # Include author info if existant and they chose to share their info
        sender = "@[" + str(instance.author.facebookuser.social_id) + "]"
    else:
        sender = "Alguém"
    template = sender + " acaba de enviar um Spotted pra você!"
    href = reverse('spotteds:view_spotted', kwargs={'spottedid': instance.spotted_count})
    userid = instance.target.facebookuser.social_id

    try:
        app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)
    except GraphAPIError as e:
        if 'Only web canvas apps can send app notifications' in getattr(e, 'message', ''):
            print(e.message.replace('\n', '\\n').replace('\r', '\\r')[:989])
        else:
            tb = traceback.format_exc()
            no_request_exception(tb, e)
