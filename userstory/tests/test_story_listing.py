from rest_framework.test import APITestCase
from userstory.tests import utils

class StoryListingTests(APITestCase):

    def setUp(self):
        utils.create_users()
        test_client = self.client
        utils.create_stories(test_client)

    def test_list_stories_as_user(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        self.assertEqual(stories_listing.status_code, 200)
        self.assertEqual(len(stories_listing.data), 2)

    def test_list_stories_as_admin(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=boss')
        self.assertEqual(stories_listing.status_code, 200)
        self.assertEqual(len(stories_listing.data), 4)

    def test_creator_view_story_detail(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=abhi' % story_id)
        self.assertEqual(story_detail.status_code, 200)
        self.assertEqual(story_detail.data['created_by_user'], 'abhi')

    def test_other_user_view_story_detail(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=arun' % story_id)
        self.assertEqual(story_detail.status_code, 401)
        self.assertEqual(story_detail.data, {'error': 'Unauthorized access'})

    def test_admin_view_story_detail(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=arun')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=boss' % story_id)
        self.assertEqual(story_detail.status_code, 200)
        self.assertEqual(story_detail.data['created_by_user'], 'arun')

    def test_user_list_stories_with_status_filter(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi&status=draft')
        self.assertEqual(len(stories_listing.data), 2)
        self.assertEqual(stories_listing.data[0]['status'], 'DRAFT')
        self.assertEqual(stories_listing.data[1]['status'], 'DRAFT')

    def test_admin_list_stories_with_status_filter(self):
        test_client = self.client
        stories_listing = test_client.get('/stories?user=boss&status=draft')
        self.assertEqual(len(stories_listing.data), 4)
        self.assertEqual(stories_listing.data[2]['status'], 'DRAFT')
        self.assertEqual(stories_listing.data[3]['status'], 'DRAFT')