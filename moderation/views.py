from django.shortcuts import render, HttpResponse, get_object_or_404
from spotteds.models import PendingSpotted, Spotted
from django.http import JsonResponse
from api.api_interface import api_process_approved, api_process_rejected, api_reject_options, api_process_deleted
from .forms import WorkHourFormSet
from django.contrib import messages
from .models import Moderator
# Create your views here.


# Generic Views

def pending_spotteds(request):
    spotteds = PendingSpotted.objects.filter(polemic=False).order_by('-id')
    return render(request, 'moderation/pending_spotteds.html', {
        'spotteds': spotteds,
    })


def polemic_spotteds(request):
    spotteds = PendingSpotted.objects.filter(polemic=True).order_by('-id')
    return render(request, 'moderation/polemic_spotteds.html', {
        'spotteds': spotteds,
    })


def history_spotteds(request):
    spotteds = Spotted.objects.filter(reported='').order_by('-id')
    return render(request, 'moderation/history_spotteds.html', {
        'spotteds': spotteds,
    })


def reported_spotteds(request):
    spotteds = Spotted.objects.exclude(reported='').order_by('-id')
    return render(request, 'moderation/reported_spotteds.html', {
        'spotteds': spotteds,
    })


def change_shifts(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkHourFormSet(request.POST, instance=request.user.moderator)
        # check whether it's valid:
        if form.is_valid():
            # Aplly it
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Turnos atualizados!')
        else:
            return render(request, 'moderation/shifts.html', {'formset': form})

    # if a GET (or any other method) we'll create a blank form
    form = WorkHourFormSet(instance=request.user.moderator)
    return render(request, 'moderation/shifts.html', {'formset': form})


def show_shifts(request):
    mods = Moderator.objects.all()
    return render(request, 'moderation/show_shifts.html', {'moderators': mods})


# Action Views

def polemic_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    instance.polemic = True
    instance.save()
    return HttpResponse('Success')


def approve_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    response = api_process_approved(instance)
    if not response:
        return

    instance.post_spotted(request.user.moderator)
    return HttpResponse('Success')


def reject_options(request):
    data = api_reject_options()
    return JsonResponse(data)


def reject_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    response = api_process_rejected(instance, request.POST['option'])
    if not response:
        return

    instance.delete()
    return HttpResponse('Success')


def un_report_submit(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    instance.reported = ''
    instance.save()
    return HttpResponse('Success')


def report_submit(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    response = api_process_deleted(instance, request.POST['option'], "reported")
    if not response:
        return

    instance.remove_spotted(True)
    return HttpResponse('Success')
