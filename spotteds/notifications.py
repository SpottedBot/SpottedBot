from custom_auth.facebook_methods import get_graph as app_graph
from django.shortcuts import reverse


def author_notification(instance):
    """Author Notification

    render and send author notifications
    """

    template = "Um de seus Spotteds acaba de ser postado!"
    href = reverse('spotteds:view_spotted', kwargs={'spottedid': instance.spotted_count})
    userid = instance.author.facebookuser.social_id

    app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)


def target_notification(instance):
    """Target Notification

    render and send target notifications
    """

    if instance.author:
        # Include author info if existant
        sender = "@[" + str(instance.author.facebookuser.social_id) + "]"
    else:
        sender = "Alguém"
    template = sender + " acaba de enviar um Spotted pra você!"
    href = reverse('spotteds:view_spotted', kwargs={'spottedid': instance.spotted_count})
    userid = instance.target.facebookuser.social_id

    app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)
