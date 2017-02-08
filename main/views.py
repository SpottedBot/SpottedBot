from django.shortcuts import render, redirect, render_to_response, get_object_or_404, HttpResponse
from spotteds.forms import PendingSpottedForm
from custom_auth.models import FacebookUser
from django.http import JsonResponse
from .forms import ContactForm, ReportForm
from django.contrib import messages
from django.conf import settings
from spotteds.models import Spotted, PendingSpotted
from django.contrib.auth.models import User
from django.template import RequestContext
from api.api_interface import api_process_deleted, api_my_delete_options, api_forme_delete_options


def index(request, contactform=None, spottedform=None, reportform=None):
    if spottedform is None:
        spottedform = PendingSpottedForm()
    if contactform is None:
        contactform = ContactForm()
    if reportform is None:
        reportform = ReportForm()

    spotteds = Spotted.objects.all()
    users = User.objects.all()

    return render(request, 'main/index.html', {
        'spottedform': spottedform,
        'contactform': contactform,
        'reportform': reportform,
        'contactemail': settings.DEFAULT_CONTACT_EMAIL,
        'spotteds': spotteds,
        'users': users,
    })


def prefetch_facebook_usernames(request):
    names = [obj.name for obj in FacebookUser.objects.all()]
    return JsonResponse(names, safe=False)


def contact(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            form.send()
            messages.add_message(request, messages.SUCCESS, 'Mensagem enviada com sucesso!')
        else:
            return index(request, contactform=form)
    return redirect('index')


def report(request):

    if request.method == 'POST':

        form = ReportForm(request.POST)

        if form.is_valid():
            form.report()
            messages.add_message(request, messages.SUCCESS, 'Spotted reportado!')
        else:
            return index(request, reportform=form)
    return redirect('index')


def delete_spotted(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])

    if instance.author == request.user:
        by = "author"
    elif instance.target == request.user:
        by = "target"
    else:
        return

    response = api_process_deleted(instance, request.POST['option'], by)
    if not response:
        return

    instance.remove_spotted(True)
    return HttpResponse('Success')


def dashboard(request):

    pendingspotteds = PendingSpotted.objects.filter(polemic=False)
    polemicspotteds = PendingSpotted.objects.filter(polemic=True)
    reportedspotteds = Spotted.objects.exclude(reported='')
    regularspotteds = Spotted.objects.filter(reported='')
    formespotteds = request.user.targeted.filter(dismissed=False)

    # If a moderator access the dashboard, log their action
    try:
        mod = request.user.moderator
        mod.log_action()
    except:
        pass
    return render(request, 'main/dashboard.html', {
        'pendingspotteds': pendingspotteds,
        'polemicspotteds': polemicspotteds,
        'reportedspotteds': reportedspotteds,
        'regularspotteds': regularspotteds,
        'formespotteds': formespotteds,
    })


def my_spotteds(request):
    return render(request, 'main/users/my_spotteds.html')


def my_delete_options(request):
    data = api_my_delete_options()
    return JsonResponse(data)


def forme_spotteds(request):
    return render(request, 'main/users/forme_spotteds.html')


def forme_delete_options(request):
    data = api_forme_delete_options()
    return JsonResponse(data)


def dismiss_submit(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    instance.dismissed = True
    instance.save()
    return HttpResponse('Success')


def search(request):
    return render(request, 'main/search.html')


# show 404 page
def handler404(request):
    response = render_to_response('main/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


# show 500 page
def handler500(request):
    response = render_to_response('main/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
