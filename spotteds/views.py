from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.http import Http404
from .models import Spotted
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.


@method_decorator([xframe_options_exempt, csrf_exempt], name='dispatch')
class ViewSpotted(DetailView):
    model = Spotted
    template_name = 'spotteds/view_spotted.html'
    context_object_name = 'spotted'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = int(self.kwargs.get(self.pk_url_kwarg)) - int(settings.INITIAL_COUNT)
        print(pk)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class ListSpotteds(ListView):
    model = Spotted
    paginate_by = 2
    template_name = 'spotteds/list_spotteds.html'
    context_object_name = 'spotteds'

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if not search:
            return self.model.objects.all()
        return self.model.objects.filter(message__icontains=search)
