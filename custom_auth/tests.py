from django.test import TestCase
from .models import FacebookUser
from django.contrib.auth.models import User

# Create your tests here.


class TestFacebookUser(TestCase):

    def test_manual_user_creation(self):
        user = User.objects.create_user('user1')
        FacebookUser.objects.create(
            user=user,
            access_token='abc123',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        self.assertTrue(FacebookUser.objects.filter(user=user).exists())

    def test_create_method(self):
        FacebookUser.create_or_update(
            access_token='abc123',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        self.assertTrue(FacebookUser.objects.filter(social_id='1234').exists())

    def test_cascade_delete(self):
        FacebookUser.create_or_update(
            access_token='abc123',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        FacebookUser.objects.get(social_id='1234').user.delete()
        self.assertFalse(FacebookUser.objects.filter(social_id='1234').exists())

    def test_users_same_name(self):
        FacebookUser.create_or_update(
            access_token='abc123',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        FacebookUser.create_or_update(
            access_token='abc123',
            social_id='12345',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        self.assertEqual(FacebookUser.objects.filter(name='user joe').count(), 2)
        self.assertTrue(User.objects.filter(username='user joe_0').exists())
        self.assertTrue(User.objects.filter(username='user joe_1').exists())

    def test_update_user(self):
        FacebookUser.create_or_update(
            access_token='abc123',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joe',
            link='https://facebook.com'
        )
        self.assertEqual(FacebookUser.objects.get(social_id='1234').access_token, 'abc123')
        self.assertEqual(FacebookUser.objects.get(social_id='1234').name, 'user joe')
        FacebookUser.create_or_update(
            access_token='abc1234',
            social_id='1234',
            expires=100,
            first_name='user',
            name='user joes',
            link='https://facebook.com'
        )
        self.assertEqual(FacebookUser.objects.get(social_id='1234').access_token, 'abc1234')
        self.assertEqual(FacebookUser.objects.get(social_id='1234').name, 'user joes')
