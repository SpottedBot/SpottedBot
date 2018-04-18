import requests
from django.shortcuts import reverse
from django.conf import settings


def get_settings():

    api_url = settings.SPOTTED_API_URL
    token = settings.SPOTTED_API_SECRET
    headers = {'Authorization': 'Token ' + token}
    return api_url, token, headers


def api_process_new_post(instance):
    """
    Process new post through the API
    """

    api_url, token, headers = get_settings()

    # Payload
    data = {
        'message': instance.message,
        'is_safe': instance.is_attachment_safe,
        'has_attachment': instance.has_attachment
    }

    # Resolve URL
    url = api_url + reverse('api:process_new_post')

    # Send payload to API
    response = requests.post(url, headers=headers, data=data)
    # If ok,
    if response.status_code == requests.codes.ok:
        # Check for the required response data
        try:
            # If the API has decided that the post should be posted right away, do that
            if response.json()['action'] == 'approve':
                instance.suggestion = response.json()['suggestion']
                instance.api_id = response.json()['api_id']
                instance.save()
                instance.post_spotted()

                return True

            # If the API has decided that the post should be rejected, do that
            elif response.json()['action'] == 'reject':
                instance.delete()
                return True

            # Send to human evaluation, if needed
            elif response.json()['action'] == 'moderation':
                instance.suggestion = response.json()['suggestion']
                instance.api_id = response.json()['api_id']
                instance.save()
                return True
        except Exception as e:
            print(e)
    # Abort and delete post if the response is invalid
    instance.delete()
    return False


# Process
def api_process_approved(instance):
    """
    Process an approved post through the API
    """

    api_url, token, headers = get_settings()

    data = {
        'api_id': instance.api_id
    }

    url = api_url + reverse('api:process_approved')

    r = requests.post(url, headers=headers, data=data)

    if r.status_code == requests.codes.ok:
        instance.api_id = r.json()['api_id']
        instance.save()
    elif r.status_code != 403:
        instance.delete()
    # Returns True if the status code is OK, False otherwise
    return r.status_code == requests.codes.ok


def api_process_rejected(instance, reason):
    """
    Process a rejected post through the API
    """

    api_url, token, headers = get_settings()

    data = {
        'reason': reason,
        'api_id': instance.api_id,
        'suggestion': instance.suggestion
    }

    url = api_url + reverse('api:process_rejected')

    r = requests.post(url, headers=headers, data=data)

    if r.status_code != 403:
        instance.delete()

    return r.status_code == requests.codes.ok


def api_reject_options():
    """Get list of reject options

    These options will be shown at the moderator's view when trying to reject a post
    """

    api_url, token, headers = get_settings()

    url = api_url + reverse('api:reject_options')

    r = requests.get(url, headers=headers)

    return r.json()


def api_process_deleted(instance, reason, by):
    """
    Process a deleted post through the API
    """

    api_url, token, headers = get_settings()

    data = {
        'reason': reason,
        'by': by,
        'api_id': instance.api_id
    }

    url = api_url + reverse('api:process_deleted')

    r = requests.post(url, headers=headers, data=data)

    return r.status_code == requests.codes.ok


def api_my_delete_options():
    """Get list of 'my' delete options

    These options will be shown at the user's view when trying to delete a post they own
    """

    api_url, token, headers = get_settings()

    url = api_url + reverse('api:my_delete_options')

    r = requests.get(url, headers=headers)

    return r.json()


def api_forme_delete_options():
    """Get list of 'forme' delete options

    These options will be shown at the user's view when trying to delete a post sent to them
    """

    api_url, token, headers = get_settings()

    url = api_url + reverse('api:forme_delete_options')

    r = requests.get(url, headers=headers)

    return r.json()


def api_get_update_coinhive():
    api_url, token, headers = get_settings()

    url = api_url + reverse('api:coinhivestats')

    r = requests.get(url, headers=headers)

    return r.json()
