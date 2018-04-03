from django.test import TestCase, override_settings
from spotteds.models import Spotted, PendingSpotted
from . import api_interface

# Create your tests here.


@override_settings(TEST_MODE=True)
class TestModerationAPI(TestCase):

    def test_new_valid_spotted(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        resp = api_interface.api_process_new_post(spotted)
        self.assertTrue(resp)
        # assert that the spotted was posted
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertTrue(Spotted.objects.filter(api_id=-1).exists())

    def test_new_valid_spotted_wrong_token(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_SECRET='abc'):
            resp = api_interface.api_process_new_post(spotted)
        self.assertFalse(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertFalse(Spotted.objects.filter(api_id=-1).exists())

    def test_new_valid_spotted_wrong_url(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_URL='https://google.com/'):
            resp = api_interface.api_process_new_post(spotted)
        self.assertFalse(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertFalse(Spotted.objects.filter(api_id=-1).exists())

    def test_new_invalid_spotted(self):
        spotted = PendingSpotted.objects.create(message="jogo do pontinho", attachment_safe=True)
        resp = api_interface.api_process_new_post(spotted)
        self.assertTrue(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertFalse(Spotted.objects.filter(api_id=-1).exists())

    def test_new_uncertain_spotted(self):
        spotted = PendingSpotted.objects.create(message="Eu sempre quis saber", attachment_safe=True)
        resp = api_interface.api_process_new_post(spotted)
        self.assertTrue(resp)
        self.assertTrue(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertFalse(Spotted.objects.filter(api_id=-1).exists())

    def test_process_approved(self):
        spotted = PendingSpotted.objects.create(message="Eu sempre quis saber", attachment_safe=True)
        resp = api_interface.api_process_approved(spotted)
        self.assertTrue(resp)
        self.assertTrue(PendingSpotted.objects.get(id=spotted.id).api_id == -1)

    def test_process_approved_wrong_token(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_SECRET='abc'):
            resp = api_interface.api_process_approved(spotted)
        self.assertFalse(resp)
        self.assertTrue(PendingSpotted.objects.filter(id=spotted.id).exists())
        self.assertFalse(PendingSpotted.objects.get(id=spotted.id).api_id == -1)

    def test_process_approved_wrong_url(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_URL='https://google.com/'):
            resp = api_interface.api_process_approved(spotted)
        self.assertFalse(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())

    def test_process_rejected(self):
        spotted = PendingSpotted.objects.create(message="Eu sempre quis saber", attachment_safe=True)
        resp = api_interface.api_process_rejected(spotted, 'Repetido')
        self.assertTrue(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())

    def test_process_rejected_wrong_token(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_SECRET='abc'):
            resp = api_interface.api_process_rejected(spotted, 'Repetido')
        self.assertFalse(resp)
        self.assertTrue(PendingSpotted.objects.filter(id=spotted.id).exists())

    def test_process_rejected_wrong_url(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_URL='https://google.com/'):
            resp = api_interface.api_process_rejected(spotted, 'Repetido')
        self.assertFalse(resp)
        self.assertFalse(PendingSpotted.objects.filter(id=spotted.id).exists())


class TestUserControlAPI(TestCase):

    def test_process_deleted(self):
        spotted = Spotted.objects.create(message="Eu sempre quis saber")
        resp = api_interface.api_process_deleted(spotted, 'Repetido', 'author')
        self.assertTrue(resp)

    def test_process_deleted_wrong_token(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_SECRET='abc'):
            resp = api_interface.api_process_deleted(spotted, 'Repetido', 'author')
        self.assertFalse(resp)

    def test_process_deleted_wrong_url(self):
        spotted = PendingSpotted.objects.create(message="beija garotas?", attachment_safe=True)
        with self.settings(SPOTTED_API_URL='https://google.com/'):
            resp = api_interface.api_process_deleted(spotted, 'Repetido', 'author')
        self.assertFalse(resp)


class TestOptionsAPI(TestCase):

    def test_reject_options(self):
        resp = api_interface.api_reject_options()
        self.assertTrue(resp)

    def test_forme_delete_options(self):
        resp = api_interface.api_forme_delete_options()
        self.assertTrue(resp)

    def test_my_delete_options(self):
        resp = api_interface.api_my_delete_options()
        self.assertTrue(resp)


class TestCoinhiveAPI(TestCase):

    def test_get_update_coinhive(self):
        resp = api_interface.api_get_update_coinhive()
        self.assertTrue(resp)
