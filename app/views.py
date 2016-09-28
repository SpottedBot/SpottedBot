from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from social.apps.django_app.default.models import UserSocialAuth

from app.models import Spotted
from helpers import facebook_utils, page_utils, template_vars, publishing, spam_utils


# display the index page
def index(request):
    temp_vars = template_vars.load_index(request.user)
    return render(request, 'index.html', {'vars': temp_vars})


# deprecated (?)
# @login_required(login_url='/')
# def home(request):
#     return render_to_response(index)


# logout handler
def logout(request):
    auth_logout(request)
    return redirect('/')


# show 404 page
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


# show 500 page
def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


#   generic request actions
# ToDo
# Assign these actions to the templates


# post a spotted and add it to the DB
def post_spotted(request):
    if request.method == 'GET':
        return redirect('/')

    f_fields, temp_vars = publishing.get_values(request)

    if not publishing.cap_check(request.POST['g-recaptcha-response']):
        messages.add_message(request, messages.ERROR,
                             'Captcha inválido!')
        return render(request, 'index.html', {'vars': temp_vars})

    posted = page_utils.post(f_fields['message'], f_fields['author'], f_fields['target'], f_fields['attachment'])

    messages.add_message(request, messages.SUCCESS,
               '<b><a class="is-link button" target="_blank" href="http://facebook.com/%s">Spotted enviado!!</a></b>'
                         % posted.post_id)
    return redirect('/')


# if the author so desires, delete a given spotted(from page and DB)
def delete_spotted(request):  # from author
    if request.method == 'GET' or not request.user.is_authenticated():
        return redirect('/')

    s = Spotted.objects.get(author=request.user)
    if request.POST['id'] != s.id:
        messages.add_message(request, messages.ERROR,
                             'Você não tem permissão para isso!')
        return redirect('/')

    page_utils.delete(request.POST['id'], True)

    messages.add_message(request, messages.SUCCESS,
                         'Spotted deletado!')
    return redirect('/profile/')


# if the target requires, dismiss, without setting as spam, a given spotted
# dismissed spotteds won't appear on the target's index page
def dismiss_spotted(request):    # from target
    if request.method == 'GET' or not request.user.is_authenticated():
        return redirect('/')

    s = Spotted.objects.get(id=request.POST['id'])
    s.dismissed = True
    s.save()

    messages.add_message(request, messages.SUCCESS,
                         'Spotted dispensado!')
    return redirect('/')


# if the target requires, report(set as spam) a given spotted immediately
def report_spotted(request):    # from target
    if request.method == 'GET' or not request.user.is_authenticated():
        return redirect('/')

    usa = UserSocialAuth.objects.get(user=request.user)
    s = Spotted.objects.get(id=request.POST['id'])
    if request.user.profile.global_id != s.target:
        messages.add_message(request, messages.ERROR,
                             'Você não tem permissão para isso!')
        return redirect('/')

    page_utils.delete(spotted_id, False)

    messages.add_message(request, messages.SUCCESS,
                         'Spotted reportado!<b>Sentimos muito pela inconveniência.')
    return redirect('/')


# load moderation page
def moderation(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.ERROR,
                             'Você não tem permissão para isso!')
        return redirect('/')
    temp_vars = template_vars.load_mod()
    return render(request, 'mod.html', {'vars': temp_vars})


# unspam spotted, given a post id and the user being staff
def unspam_spotted(request):
    if request.method == 'GET' or not request.user.is_authenticated():
        return redirect('/')

    if not request.user.is_staff:
        messages.add_message(request, messages.ERROR,
                             'Você não tem permissão para isso!')
        return redirect('/')

    spam_utils.un_spam(request.POST['id'])
    return redirect('/mod/')


# load profile page
def profile(request):
    if request.method == 'GET' or not request.user.is_authenticated():
        return redirect('/')
    temp_vars = template_vars.load_profile(request.user)
    return render(request, 'profile.html', {'vars': temp_vars})
