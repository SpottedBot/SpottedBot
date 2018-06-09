from django.shortcuts import HttpResponse, get_object_or_404
from django.views.generic import View, ListView, FormView
from django.utils.decorators import method_decorator
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db import transaction

from spotteds.models import PendingSpotted, Spotted
from .models import Moderator

from api.api_interface import api_process_approved, api_process_rejected, api_reject_options, api_process_deleted
from .forms import WorkHourFormSet
from main.mixins import ModOnlyMixin
# Create your views here.


# Generic Views


class ModView(ModOnlyMixin, ListView):
    context_object_name = 'spotteds'


class PendingSpottedsView(ModView):
    """Pending Spotteds.

    render pending spotteds view
    """

    template_name = 'moderation/pending_spotteds.html'
    model = PendingSpotted

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(polemic=False)


class PolemicSpottedsView(ModView):
    """Polemic Spotteds.

    render Polemic spotteds view
    """

    template_name = 'moderation/polemic_spotteds.html'
    model = PendingSpotted

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(polemic=True)


class HistorySpottedsView(ModView):
    """Spotted History.

    render spotted historys view
    """

    template_name = 'moderation/history_spotteds.html'
    model = Spotted

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(reported='')[:500]


class ReportedSpottedsView(ModView):
    """Reported Spotteds.

    render reported spotteds view
    """

    template_name = 'moderation/reported_spotteds.html'
    model = Spotted

    def get_queryset(self, **kwargs):
        return self.model.objects.exclude(reported='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class ChangeShifts(ModOnlyMixin, FormView):
    form_class = WorkHourFormSet
    template_name = 'moderation/shifts.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.moderator
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Turnos atualizados!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = context['form']
        return context


class ShowShifts(ModOnlyMixin, ListView):
    """Show Shifts.

    render show shifts view
    """

    template_name = 'moderation/show_shifts.html'
    model = Moderator
    context_object_name = 'moderators'

    def get_queryset(self, **kwargs):
        return self.model.objects.all()


# Action Views

class PolemicSubmit(ModOnlyMixin, View):
    """Polemic Submit.

    process the submission of a polemic spotted
    """

    def post(self, request):
        instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
        instance.polemic = True
        instance.save()
        return HttpResponse('Success')


@method_decorator(transaction.atomic, name='dispatch')
class ApproveSubmit(ModOnlyMixin, View):
    """Approve Submit.

    process the approval of a pending spotted
    """

    def post(self, request):
        instance = PendingSpotted.objects.select_for_update().get(id=request.POST['id'])
        response = api_process_approved(instance)
        if response:
            instance.post_spotted(request.user.moderator)

        return HttpResponse('Success')


class RejectOptions(ModOnlyMixin, View):
    """Reject Options.

    retrieve reject options from api
    """

    def get(self, request):
        data = api_reject_options()
        return JsonResponse(data)


@method_decorator(transaction.atomic, name='dispatch')
class RejectSubmit(ModOnlyMixin, View):
    """Reject Submit.

    process the rejection of a pending spotted
    """

    def post(self, request):
        instance = PendingSpotted.objects.select_for_update().get(id=request.POST['id'])
        api_process_rejected(instance, request.POST['option'])
        return HttpResponse('Success')


class UnReportSubmit(ModOnlyMixin, View):
    """Un Report Submit.

    process the un-reporting of a reported spotted
    """

    def post(self, request):
        instance = get_object_or_404(Spotted, id=request.POST['id'])
        instance.reported = ''
        instance.save()
        return HttpResponse('Success')


@method_decorator(transaction.atomic, name='dispatch')
class ReportSubmit(ModOnlyMixin, View):
    """Report Submit.

    process the deletion of a reported spotted
    """

    def post(self, request):
        instance = get_object_or_404(Spotted, id=request.POST['id'])
        response = api_process_deleted(instance, request.POST['option'], "reported")
        if not response:
            raise Http404
        instance.remove_spotted(True)
        return HttpResponse('Success')
