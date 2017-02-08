from django.shortcuts import reverse, redirect, get_object_or_404, render
from .forms import PendingSpottedForm
from django.contrib import messages
from .models import Spotted
from main.views import index
from api.api_interface import api_process_new_post
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.


def submit_spotted(request):
    # User submitted spotted

    if request.method == 'POST':
        form = PendingSpottedForm(request.POST)

        if form.is_valid():
            instance = form.save(request.user)

            if api_process_new_post(instance):
                messages.add_message(request, messages.SUCCESS, 'Spotted enviado!')
            else:
                messages.add_message(request, messages.ERROR, 'Oops! Erro na comunicação com a API!')
    else:
        form = PendingSpottedForm()
    return index(request, spottedform=form)


@xframe_options_exempt
@csrf_exempt
def view_spotted(request, spottedid):
    print("started")
    try:
        count = int(spottedid) - int(settings.INITIAL_COUNT)
        spotted = Spotted.objects.get(id=count)
    except:
        spotted = get_object_or_404(Spotted, id=spottedid)
    print("finished")
    return render(request, 'spotteds/view_spotted.html', {'spotted': spotted})
