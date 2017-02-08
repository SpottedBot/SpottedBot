import requests
from django.shortcuts import reverse
from django.conf import settings

api_url = settings.SPOTTED_API_URL
token = settings.SPOTTED_API_SECRET
headers = {'Authorization': 'Token ' + token}


def api_process_new_post(instance):
    data = {
        'message': instance.message,
        'is_safe': instance.is_attachment_safe,
    }

    url = api_url + reverse('api:process_new_post')

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == requests.codes.ok:

        try:
            if response.json()['action'] == 'approve':
                instance.suggestion = response.json()['suggestion']
                instance.api_id = response.json()['api_id']
                instance.save()
                instance.post_spotted()
                return True

            elif response.json()['action'] == 'reject':
                instance.delete()
                return True

            elif response.json()['action'] == 'moderation':
                instance.suggestion = response.json()['suggestion']
                instance.api_id = response.json()['api_id']
                instance.save()
                return True
        except:
            pass

    instance.delete()
    return False


def api_process_approved(instance):
    data = {
        'api_id': instance.api_id
    }

    url = api_url + reverse('api:process_approved')

    r = requests.post(url, headers=headers, data=data)

    if r.status_code == requests.codes.ok:
        instance.api_id = r.json()['api_id']
        instance.save()

    return r.status_code == requests.codes.ok


def api_process_rejected(instance, reason):
    data = {
        'reason': reason,
        'api_id': instance.api_id,
        'suggestion': instance.suggestion
    }

    url = api_url + reverse('api:process_rejected')

    r = requests.post(url, headers=headers, data=data)

    return r.status_code == requests.codes.ok


def api_reject_options():
    url = api_url + reverse('api:reject_options')

    r = requests.get(url, headers=headers)

    return r.json()


def api_process_deleted(instance, reason, by):
    data = {
        'reason': reason,
        'by': by,
        'api_id': instance.api_id
    }

    url = api_url + reverse('api:process_deleted')

    r = requests.post(url, headers=headers, data=data)

    return r.status_code == requests.codes.ok


def api_my_delete_options():
    url = api_url + reverse('api:my_delete_options')

    r = requests.get(url, headers=headers)

    return r.json()


def api_forme_delete_options():
    url = api_url + reverse('api:forme_delete_options')

    r = requests.get(url, headers=headers)

    return r.json()
