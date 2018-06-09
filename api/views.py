from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
# Create your views here.


# The views here are for debugging of requests and to mimic the behavior of the API


@method_decorator(csrf_exempt, name='dispatch')
class CSRFExemptView(View):
    pass


class ProcessNewPost(CSRFExemptView):
    def post(self, request):
        print(request.POST['message'])
        return JsonResponse({'action': 'moderation', 'suggestion': ''})


class ProcessApproved(CSRFExemptView):
    def post(self, request):
        print('API Approved ' + request.POST['message'])
        return HttpResponse('')


class ProcessRejected(CSRFExemptView):
    def post(self, request):
        print('API Reject ' + request.POST['reason'])
        return HttpResponse('')


class ProcessDeleted(CSRFExemptView):
    def post(self, request):
        print('API Delete ' + request.POST['by'])
        return HttpResponse('')


class RejectOptions(CSRFExemptView):
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

    def get(self, request):
        return JsonResponse(self.data)


class MyDeleteOptions(CSRFExemptView):
    data = {
        "opt_1": "Digitei errado",
        "opt_2": "Crush errado",
        "opt_3": "Me arrependi",
        "opt_4": "Mais",
        "opt_5": "Prefiro não dizer",
        "opt_8": "Outro"
    }

    def get(self, request):
        return JsonResponse(self.data)


class ForMeDeleteOptions(CSRFExemptView):
    data = {
        "opt_1": "Ofensivo",
        "opt_2": "Sexual",
        "opt_3": "Inadequado",
        "opt_4": "Mais",
        "opt_5": "Comprometidx",
        "opt_6": "Prefiro não dizer",
        "opt_8": "Outro"
    }

    def get(self, request):
        return JsonResponse(self.data)


class CoinHiveStats(CSRFExemptView):
    def get(self, request):
        print('Got coinhivestats')
        return HttpResponse('')


class SubmitMessageLog(CSRFExemptView):
    def post(self, request):
        print('Submitted message log')
        return HttpResponse('')


class ProcessRawBotMessage(CSRFExemptView):
    def post(self, request):
        print('Processing the message', request.POST['message'])
        return HttpResponse({'result_status': True, 'result': 'Base solution'})
