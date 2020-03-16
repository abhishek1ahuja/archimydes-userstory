from django.test.utils import setup_test_environment
from django.test import Client
from django.test import TestCase
from rest_framework.test import APITestCase
from userstory.tests import utils
from django.urls import reverse

from userstory.models import *

# setup_test_environment()
# test_client = Client()

class StoryCreateTests(APITestCase):

    def setUp(self):
        utils.create_users()

    def test_list_stories_initial(self):
        response = self.client.get('/stories?user=abhi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])


    def test_create_story_and_retrieve_by_creator(self):
        story = utils.make_story(summary='sample story 1', story_type='testing')
        story_create = self.client.post('/stories?user=abhi', data=story, format='json')
        story_retrieve = self.client.get('/stories?user=abhi')
        self.assertEqual(story_retrieve.status_code, 200)
        self.assertContains(story_retrieve, "sample story 1")

    def test_create_story_and_retrieve_by_admin_user(self):
        story = utils.make_story(summary='sample story 2', story_type='testing')
        story_create = self.client.post('/stories?user=abhi', data=story, format='json')
        story_retrieve = self.client.get('/stories?user=boss')
        self.assertEqual(story_retrieve.status_code, 200)
        self.assertContains(story_retrieve, "sample story 2")

    def test_create_story_and_retrive_by_other_user(self):
        story = utils.make_story(summary='sample story 2', story_type='testing')
        story_create = self.client.post('/stories?user=abhi', data=story, format='json')
        story_retrieve = self.client.get('/stories?user=arun')
        self.assertEqual(story_retrieve.status_code, 200)
        self.assertEqual(story_retrieve.data, [])