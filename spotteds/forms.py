from django import forms
from .models import PendingSpotted
from custom_auth.models import FacebookUser
from captcha.fields import ReCaptchaField


class PendingSpottedForm(forms.ModelForm):
    """PendingSpottedForm
    Form for the submission of new spotteds
    """
    anonymous = forms.BooleanField(required=False, label='Anônimo?')
    target_name = forms.CharField(required=False, label='Nome do(a) Crush', widget=forms.TextInput(attrs={'class': 'typeahead', 'placeholder': 'Crush Santos da Silva'}))
    captcha = ReCaptchaField()

    class Meta:
        model = PendingSpotted
        fields = ['message', 'attachment', 'public']
        labels = {
            'message': 'Mensagem',
            'attachment': 'Anexo (GIFs, links, etc)',
            'public': 'Público?'
        }
        widgets = {
            'attachment': forms.TextInput(attrs={'placeholder': 'http://crush.com/vamo_se_pegar.gif'})
        }

    def clean_target_name(self):
        # Get target obj if applicable

        target_name = self.cleaned_data.get('target_name')
        if target_name:
            try:
                target = FacebookUser.objects.get(name=target_name)
                return target.user
            except:
                raise forms.ValidationError(target_name + " ainda não está cadastrado(a). Verifique sua digitação ou deixe em branco.")
        return None

    def save(self, author):
        # Apply author and target if applicable

        instance = super(PendingSpottedForm, self).save(commit=False)
        anonymous = self.cleaned_data['anonymous']
        target = self.cleaned_data['target_name']

        if anonymous is not True and author.is_authenticated():
            instance.author = author

        if target is not None:
            instance.target = target

        instance.save()
        return instance
