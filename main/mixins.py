from django.http import JsonResponse
from .decorators import custom_user_passes_test
from moderation.decorators import is_moderator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View


class AjaxableResponseMixin:
    """Mixin to add AJAX support to a form.

    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        if self.request.is_ajax():
            data = form.response_data
            return JsonResponse(data)
        else:
            return super().form_valid(form)


@method_decorator(custom_user_passes_test(is_moderator), name='dispatch')
class ModOnlyMixin(View):
    pass


@method_decorator(login_required, name='dispatch')
class LoginRequiredMixin(View):
    pass
