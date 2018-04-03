from django.test import TestCase, override_settings
from contextlib import contextmanager
from smtplib import SMTPException
from main.forms import ContactForm, ReportForm
from spotteds.models import Spotted

# Create your tests here.


class ExtTestCase(TestCase):

    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))


class TestContactForm(ExtTestCase):

    def test_contact_form(self):
        form = ContactForm(data={'name': 'John Doe', 'email': 'example@example.com', 'subject': 'Test', 'text': 'this is a test'})
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form = ContactForm(data={'name': 'John Doe', 'email': 'not_an_email', 'subject': 'Test', 'text': 'this is a test'})
        self.assertFalse(form.is_valid())

    def test_contact_send(self):
        form = ContactForm(data={'name': 'John Doe', 'email': 'example@example.com', 'subject': 'Test', 'text': 'this is a test'})
        with override_settings(CONTACT_EMAIL='adm@example.com'):
            form.is_valid()
            with self.assertNotRaises(SMTPException):
                form.send()


class TestReportForm(TestCase):

    def setUp(self):
        Spotted.objects.create(message="test")

    def test_report_form(self):
        form = ReportForm(data={'number': 1, 'text': 'this is a test'})
        with override_settings(INITIAL_COUNT=0):
            self.assertTrue(form.is_valid())

    def test_report_form_invalid(self):
        form = ReportForm(data={'number': '2', 'text': 'this is a test'})
        with override_settings(INITIAL_COUNT=0):
            self.assertFalse(form.is_valid())

    def test_report_submit(self):
        form = ReportForm(data={'number': 1, 'text': 'this is a test'})
        with override_settings(INITIAL_COUNT=0):
            form.is_valid()
            form.report()
            self.assertEqual(Spotted.objects.get(id=1).reported, 'this is a test')
