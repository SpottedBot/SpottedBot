from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import TokenForm
# Create your views here.


# The views here are for debugging of requests and to mimic the behavior of the API


@csrf_exempt
def process_new_post(request):

    print(request.POST['message'])

    return JsonResponse({'action': 'moderation', 'suggestion': ''})


@csrf_exempt
def process_approved(request):
    print('API Approved ' + request.POST['message'])
    return HttpResponse('')


@csrf_exempt
def process_rejected(request):
    print('API Reject ' + request.POST['reason'])
    return HttpResponse('')


@csrf_exempt
def process_deleted(request):
    print('API Delete ' + request.POST['by'])
    return HttpResponse('')


@csrf_exempt
def reject_options(request):
    data = {
        "opt_1": "Flood",
        "opt_2": "Off-topic",
        "opt_3": "Ofensivo",
        "opt_4": "Mais",
        "opt_5": "Depressivo",
        "opt_6": "Sexual",
        "opt_7": "Spam",
        "opt_8": "Outro"
    }
    return JsonResponse(data)


@csrf_exempt
def my_delete_options(request):
    data = {
        "opt_1": "Digitei errado",
        "opt_2": "Crush errado",
        "opt_3": "Me arrependi",
        "opt_4": "Mais",
        "opt_5": "Prefiro não dizer",
        "opt_8": "Outro"
    }
    return JsonResponse(data)


@csrf_exempt
def forme_delete_options(request):
    data = {
        "opt_1": "Ofensivo",
        "opt_2": "Sexual",
        "opt_3": "Inadequado",
        "opt_4": "Mais",
        "opt_5": "Comprometidx",
        "opt_6": "Prefiro não dizer",
        "opt_8": "Outro"
    }
    return JsonResponse(data)


def get_token(request):

    if request.method == 'POST':

        form = TokenForm(request.POST)

        if form.is_valid():

            return JsonResponse(form.check(), safe=False)

    else:
        form = TokenForm()

    return render(request, 'api/token.html', {'form': form})


def coinhivestats(request):
    print('Got coinhivestats')
    return HttpResponse('')


def submit_message_log(request):
    print('Submitted message log')
    return HttpResponse('')


def process_raw_bot_message(request):
    print('Processing the message', request.POST['message'])
    return HttpResponse({'result_status': True, 'result': 'Base solution'})
