from django import forms
from .models import WorkHour, Moderator


class WorkHourForm(forms.ModelForm):
    """Work Hours Form."""

    class Meta:
        model = WorkHour
        fields = ['day', 'hour', 'duration']
        labels = {
            'day': 'Dia',
            'hour': 'Hora',
            'duration': 'Duração',
        }


WorkHourFormSet = forms.inlineformset_factory(Moderator, WorkHour, form=WorkHourForm, can_delete=True, extra=1, max_num=1000)
