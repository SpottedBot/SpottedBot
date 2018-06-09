from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import BaseFormView
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.conf import settings
import json

from .forms import ContactForm, ReportForm, ImgurForm
from spotteds.forms import PendingSpottedForm
from .multiple_forms import MultiFormsView
from .mixins import AjaxableResponseMixin, ModOnlyMixin, LoginRequiredMixin

from spotteds.models import Spotted, PendingSpotted
from django.contrib.auth.models import User
from custom_auth.models import FacebookUser
from .models import NagMessage

from api.api_interface import api_process_new_post, api_process_deleted, api_my_delete_options, api_forme_delete_options, api_get_update_coinhive

from project.manual_error_report import exception_email


class Index(MultiFormsView):
    template_name = 'main/index.html'
    form_classes = {
        'spottedform': PendingSpottedForm,
        'contactform': ContactForm,
        'reportform': ReportForm,
    }
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contactemail'] = settings.DEFAULT_CONTACT_EMAIL
        context['total_spotteds'] = Spotted.total_spotteds()
        context['total_users'] = User.objects.count()
        return context

    def contactform_form_valid(self, form):
        form.send()
        messages.add_message(self.request, messages.SUCCESS, 'Mensagem enviada com sucesso!')
        return self

    def contactform_form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erros ao enviar seu email!')
        return self

    def reportform_form_valid(self, form):
        form.report()
        messages.add_message(self.request, messages.SUCCESS, 'Spotted reportado!')
        return self

    def reportform_form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erros reportando seu spotted!')
        return self

    def spottedform_form_valid(self, form):
        instance = form.save(self.request.user)
        if api_process_new_post(instance):
            messages.add_message(self.request, messages.SUCCESS, 'Spotted enviado para moderação!')
            form = PendingSpottedForm()
        else:
            messages.add_message(self.request, messages.ERROR, 'Oops! Erro na comunicação com a API!')
        return self

    def spottedform_form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erros enviando seu spotted!')
        return self


class About(TemplateView):
    template_name = 'main/about.html'


class PrefetchFacebookUsernames(View):
    def get(self, request):
        users = []
        for user in FacebookUser.objects.all().order_by('?'):
            users.append({"name": user.name, "picture": user.thumbnail, "id": user.social_id})
        return JsonResponse(users, safe=False)


class ImgurUpload(LoginRequiredMixin, AjaxableResponseMixin, BaseFormView):
    form_class = ImgurForm


class DeleteSpotted(LoginRequiredMixin, View):
    def post(self, request):
        instance = get_object_or_404(Spotted, id=request.POST['id'])
        if instance.author == request.user:
            by = 'author'
        elif instance.target == request.user:
            by = 'target'
        else:
            raise Http404
        response = api_process_deleted(instance, request.POST['option'], by)
        if not response:
            raise Http404
            return
        try:
            # Fully delete spotted(from page and from DB)
            instance.remove_spotted(True)
        except Exception as e:
            exception_email(request, e)
            raise e
        return HttpResponse('Success')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'pendingspotteds': PendingSpotted.objects.filter(polemic=False),
            'polemicspotteds': PendingSpotted.objects.filter(polemic=True),
            'reportedspotteds': Spotted.objects.exclude(reported=''),
            'regularspotteds': Spotted.objects.filter(reported=''),
            'formespotteds': self.request.user.targeted.filter(dismissed=False),
        }
        for k, v in data.items():
            context[k] = v

        if self.request.user.is_moderator and settings.ENABLE_MOD_SHIFT:
            self.request.user.moderator.log_action()
        return context


class MySpotteds(LoginRequiredMixin, TemplateView):
    template_name = 'main/users/my_spotteds.html'


class MyDeleteOptions(LoginRequiredMixin, View):
    def get(self, request):
        data = api_my_delete_options()
        return JsonResponse(data)


class ForMeSpotteds(LoginRequiredMixin, TemplateView):
    template_name = 'main/users/forme_spotteds.html'


class ForMeDeleteOptions(LoginRequiredMixin, View):
    def get(self, request):
        data = api_forme_delete_options()
        return JsonResponse(data)


class DismissSubmit(LoginRequiredMixin, View):
    def post(self, request):
        instance = get_object_or_404(Spotted, id=request.POST['id'])
        if not instance.target == request.user:
            raise Http404
            return
        instance.dismissed = True
        instance.save()
        return HttpResponse('Success')


class Search(TemplateView):
    template_name = 'main/search.html'


class Coinhive(TemplateView):
    template_name = 'main/coinhive.html'


class GetCoinhiveStats(View):
    def get(self, request):
        data = api_get_update_coinhive()
        return JsonResponse(data)


class GetNagMessage(View):
    def get(self, request):
        nag = NagMessage.get()
        data = {
            'message': nag.message,
            'id': nag.nag_id,
            'enable': nag.enable
        }
        return JsonResponse(data)


class UpdateNagMessage(ModOnlyMixin, View):
    def post(self, request):
        NagMessage.update(request.POST['message'], json.loads(request.POST['enable']))
        return HttpResponse()


class Handler404(TemplateView):
    template_name = 'main/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


class Handler500(TemplateView):
    template_name = 'main/500.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=500)
