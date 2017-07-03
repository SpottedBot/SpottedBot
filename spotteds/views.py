from django.shortcuts import get_object_or_404, render
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
    """Submit Spotted

    User submitted a spotted
    """

    if request.method == 'POST':
        form = PendingSpottedForm(request.POST)

        if form.is_valid():
            instance = form.save(request.user)

            # Send to API
            if api_process_new_post(instance):
                messages.add_message(request, messages.SUCCESS, 'Spotted enviado para moderação!')
                form = PendingSpottedForm()
            else:
                messages.add_message(request, messages.ERROR, 'Oops! Erro na comunicação com a API!')
    else:
        form = PendingSpottedForm()
    return index(request, spottedform=form)


@xframe_options_exempt
@csrf_exempt
def view_spotted(request, spottedid):
    """View Spotted

    Display spotted info. Certain fields may only be viewed by the author or target
    """

    try:
        count = int(spottedid) - int(settings.INITIAL_COUNT)
        spotted = Spotted.objects.get(id=count)
    except:
        spotted = get_object_or_404(Spotted, id=spottedid)
    return render(request, 'spotteds/view_spotted.html', {'spotted': spotted})
