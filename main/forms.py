from django import forms
from django.core.mail import send_mail
from django.conf import settings
from spotteds.models import Spotted


class ContactForm(forms.Form):
    """Contact Form

    Contact form fields and methods
    """

    name = forms.CharField(label='Seu nome', max_length=30)
    email = forms.EmailField(label='Seu email')
    subject = forms.CharField(label='Assunto', max_length=30)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}), label='Mensagem')

    def send(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        text = self.cleaned_data['text']

        send_mail(
            subject,
            name + ', ' + email + ', enviou um email pelo site do Spotted:\n\n---------\n' + text + '\n---------\n\nLove,\nSpotted Bot.',
            email,
            [settings.DEFAULT_CONTACT_EMAIL, email]
        )


class ReportForm(forms.Form):
    """Report Form

    Report form fields and methods
    """

    number = forms.IntegerField(label='Número do Spottd')
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}), label='Mensagem', max_length=1000, required=True)

    def clean_number(self):

        data = self.cleaned_data.get('number')
        try:
            val = int(data) - int(settings.INITIAL_COUNT)
            i = Spotted.objects.get(id=val)
        except:
            raise forms.ValidationError(
                "Não existe Spotted com esse ID"
            )
        return i

    def report(self):
        instance = self.cleaned_data['number']
        text = self.cleaned_data['text']

        instance.reported = text
        instance.save()
