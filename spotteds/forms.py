from django import forms
from .models import PendingSpotted
from custom_auth.models import FacebookUser
from captcha.fields import ReCaptchaField


class PendingSpottedForm(forms.ModelForm):
    """PendingSpottedForm
    Form for the submission of new spotteds
    """
    target_name = forms.CharField(required=False, label='Nome do(a) Crush', widget=forms.TextInput(attrs={'class': 'typeahead', 'placeholder': 'Crush Santos da Silva'}))
    target_id = forms.CharField(required=False, widget=forms.HiddenInput())
    captcha = ReCaptchaField(attrs={"callback": "captchaSpottedCallback", })

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

    def clean_target_id(self):
        # Get target obj if applicable

        target_id = self.cleaned_data.get('target_id')
        target_name = self.cleaned_data.get('target_name')
        if target_id:
            try:
                target = FacebookUser.objects.get(social_id=target_id)
                if target.name == target_name:
                    return target.user
            except:
                raise forms.ValidationError(target_name + " ainda não está cadastrado(a). Verifique sua digitação ou deixe em branco.")
        return None

    def save(self, author):
        # Apply author and target if applicable

        instance = super(PendingSpottedForm, self).save(commit=False)
        target = self.cleaned_data['target_id']

        if author.is_authenticated():
            instance.author = author

        if target is not None:
            instance.target = target

        instance.save()
        return instance
