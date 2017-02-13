from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from spotteds.forms import PendingSpottedForm
from custom_auth.models import FacebookUser
from django.http import JsonResponse, Http404
from .forms import ContactForm, ReportForm
from django.contrib import messages
from django.conf import settings
from spotteds.models import Spotted, PendingSpotted
from django.contrib.auth.models import User
from api.api_interface import api_process_deleted, api_my_delete_options, api_forme_delete_options
from django.contrib.auth.decorators import login_required


def index(request, contactform=None, spottedform=None, reportform=None):
    """Index

    render index page
    """

    # Create empty forms if the were not defined on init
    if spottedform is None:
        spottedform = PendingSpottedForm()
    if contactform is None:
        contactform = ContactForm()
    if reportform is None:
        reportform = ReportForm()

    # Some other data
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


def about(request):
    """About

    render about page
    """

    return render(request, 'main/about.html')


def prefetch_facebook_usernames(request):
    names = [obj.name for obj in FacebookUser.objects.all()]
    return JsonResponse(names, safe=False)


def contact(request):
    """Contact

    process contact form submit
    """

    if request.method == 'POST':

        # retrieve posted contact form
        form = ContactForm(request.POST)

        # if it is valid
        if form.is_valid():

            # send the email
            form.send()
            messages.add_message(request, messages.SUCCESS, 'Mensagem enviada com sucesso!')
        else:

            # if it is not valid, render index with filled values
            return index(request, contactform=form)
    return redirect('index')


def report(request):
    """Report

    process report form submit
    """

    if request.method == 'POST':

        # retrieve posted report
        form = ReportForm(request.POST)

        # if it is valid
        if form.is_valid():

            # process the report
            form.report()
            messages.add_message(request, messages.SUCCESS, 'Spotted reportado!')
        else:

            # if it is not valid, render index with filled values
            return index(request, reportform=form)
    return redirect('index')


@login_required
def delete_spotted(request):
    """Delete Spotted

    process the deletion call of a spotted
    """

    # Get the deleted spotted object
    instance = get_object_or_404(Spotted, id=request.POST['id'])

    # Check if it was deleted by the author or the target
    if instance.author == request.user:
        by = "author"
    elif instance.target == request.user:
        by = "target"
    else:

        # If it was by none of them, cause error 404
        raise Http404
        return

    # Call the API
    response = api_process_deleted(instance, request.POST['option'], by)
    if not response:
        raise Http404
        return

    # Fully delete spotted(from page and from DB)
    instance.remove_spotted(True)
    return HttpResponse('Success')


@login_required
def dashboard(request):
    """Dashboard

    render dashboard
    """

    pendingspotteds = PendingSpotted.objects.filter(polemic=False)
    polemicspotteds = PendingSpotted.objects.filter(polemic=True)
    reportedspotteds = Spotted.objects.exclude(reported='')
    regularspotteds = Spotted.objects.filter(reported='')
    formespotteds = request.user.targeted.filter(dismissed=False)

    # If a moderator goes to the dashboard, log their action
    if request.user.is_moderator:
        request.user.moderator.log_action()

    return render(request, 'main/dashboard.html', {
        'pendingspotteds': pendingspotteds,
        'polemicspotteds': polemicspotteds,
        'reportedspotteds': reportedspotteds,
        'regularspotteds': regularspotteds,
        'formespotteds': formespotteds,
    })


@login_required
def my_spotteds(request):
    """My Spotteds

    render my_spotteds.html
    """

    return render(request, 'main/users/my_spotteds.html')


@login_required
def my_delete_options(request):
    """My Delete Options

    get my delete options from api
    """

    data = api_my_delete_options()
    return JsonResponse(data)


@login_required
def forme_spotteds(request):
    """For Me Spotteds

    render forme_spotteds.html
    """

    return render(request, 'main/users/forme_spotteds.html')


def forme_delete_options(request):
    """Forme Delete Options

    get forme delete options from api
    """

    data = api_forme_delete_options()
    return JsonResponse(data)


@login_required
def dismiss_submit(request):
    """Dismiss Submit

    Process submission of spotted dismissal
    """

    # Pretty straightfoward
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    if not instance.target == request.user:
        raise Http404
        return
    instance.dismissed = True
    instance.save()
    return HttpResponse('Success')


def search(request):
    """Search

    render search.html
    """

    return render(request, 'main/search.html')


# show 404 page
def handler404(request):
    response = render(request, 'main/404.html')
    response.status_code = 404
    return response


# show 500 page
def handler500(request):
    response = render(request, 'main/500.html')
    response.status_code = 500
    return response
