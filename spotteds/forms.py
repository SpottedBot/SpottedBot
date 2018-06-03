from django import forms
from .models import PendingSpotted
from custom_auth.models import FacebookUser
from captcha.fields import ReCaptchaField
from django.db.utils import ProgrammingError
from moderation.management.commands import delete_old_spotteds, inspect_database
from project.loghandler import LogHandler
from django.conf import settings


logger = LogHandler(__name__).logger


class PendingSpottedForm(forms.ModelForm):
    """PendingSpottedForm.

    Form for the submission of new spotteds
    """

    target_name = forms.CharField(required=False, label='Nome do(a) Crush', widget=forms.TextInput(attrs={'class': 'typeahead', 'placeholder': 'Crush Santos da Silva'}))
    target_id = forms.CharField(required=False, widget=forms.HiddenInput())
    share_with_crush = forms.BooleanField(required=False, initial=True, label="Informar crush que você é x autorx")

    if settings.RECAPTCHA_PUBLIC_KEY:
        captcha = ReCaptchaField(attrs={"callback": "captchaSpottedCallback", })

    class Meta:
        model = PendingSpotted
        fields = ['message', 'attachment', 'public']
        labels = {
            'message': 'Mensagem',
            'attachment': 'URL do anexo (GIFs, links, etc)',
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
        share_with_crush = self.cleaned_data['share_with_crush']

        if author.is_authenticated:
            instance.author = author

        if target is not None:
            instance.target = target

        instance.share_with_crush = share_with_crush
        try:
            instance.save()
        except ProgrammingError:
            logger.info("%s\n%s", delete_old_spotteds.delete_executer(5, True), inspect_database.inspect_executer())
            instance.save()
        return instance
