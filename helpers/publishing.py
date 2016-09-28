# evaluates the page's captcha

import requests
import os

import helpers.facebook_utils
from helpers import template_vars


# check google's response
def cap_check(grs):
    try:
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            'secret': str(os.environ.get('CAP_SECRET')),
            'response': grs,
        }
        verify_rs = requests.get(url, params=values, verify=True)
        verify_rs = verify_rs.json()
        response = verify_rs.get("success", False)
        if not response:
            return False
    except:
        return False
    return True


def get_values(request):
    message = request.POST['message']
    attachment = request.POST['attachment']
    target = helpers.facebook_utils.global_id(request.POST['target'].strip())
    author = None
    try:
        request.POST['anonymous']
    except:
        if request.user.is_authenticated():
            author = request.user
    if author:
        anon = False
    else:
        anon = True
    temp_vars = template_vars.load_index(request.user)
    temp_vars['placeholder'] = {'anonymous': anon, 'message': message, 'attachment': attachment,
                                'target': request.POST['target'].strip()}

    f_fields = {'message': message, 'attachment': attachment, 'author': author, 'target': target}
    return f_fields, temp_vars
