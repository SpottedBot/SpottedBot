from django import forms
from django.core.mail import send_mail
from django.conf import settings
from spotteds.models import Spotted
from django.template.defaultfilters import filesizeformat
from project.imgur_helper import upload


class ContactForm(forms.Form):
    """Contact Form.

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
    """Report Form.

    Report form fields and methods
    """

    number = forms.IntegerField(label='Número do Spottd')
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}), label='Mensagem', max_length=1000, required=True)

    def clean_number(self):

        data = self.cleaned_data.get('number')
        try:
            val = int(data) - int(settings.INITIAL_COUNT)
            i = Spotted.objects.get(id=val)
        except Spotted.DoesNotExist:
            raise forms.ValidationError(
                "Não existe Spotted com esse ID"
            )
        return i

    def report(self):
        instance = self.cleaned_data['number']
        text = self.cleaned_data['text']

        instance.reported = text
        instance.save()


class ContentTypeRestrictedFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        file = super().clean(*args, **kwargs)

        try:
            content_type = file.content_type
            print(content_type)
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(f'O tamanho máximo permitido é {filesizeformat(self.max_upload_size)}. Tamanho atual: {filesizeformat(file.size)}')
            else:
                raise forms.ValidationError('Arquivo deve ser uma imagem.')
        except AttributeError:
            pass

        return file


class ImgurForm(forms.Form):
    picture = ContentTypeRestrictedFileField(
        allow_empty_file=False,
        content_types=['image/jpeg', 'image/png'],
        max_upload_size=10485760
    )

    def upload(self, data=None):
        file = data or self.cleaned_data['picture']
        return upload(file.temporary_file_path())

    def clean_picture(self):
        data = super().clean()['picture']
        print(data)
        response = self.upload(data)
        if isinstance(response, forms.ValidationError):
            raise response
        self.response_data = response
        return data
