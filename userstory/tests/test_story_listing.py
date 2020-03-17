from rest_framework.test import APITestCase
from userstory.tests import utils

class StoryListingTests(APITestCase):

    def setUp(self):
        """
        creating three users for all test cases in this suite
        usernames abhi and arun are users of type user
        username boss is an admin user

        for each of the two users of type user,
        two user stories are created by them
        """
        utils.create_users()
        test_client = self.client
        utils.create_stories(test_client)

    def test_list_stories_as_user(self):
        """
        check if user is able to view list of stories created by self
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        self.assertEqual(stories_listing.status_code, 200)
        self.assertEqual(len(stories_listing.data), 2)

    def test_list_stories_as_admin(self):
        """
        check if admin is able to view list of stories created by all users
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=boss')
        self.assertEqual(stories_listing.status_code, 200)
        self.assertEqual(len(stories_listing.data), 4)

    def test_creator_view_story_detail(self):
        """
        check if user is able to view story detail
        of story created by self
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=abhi' % story_id)
        self.assertEqual(story_detail.status_code, 200)
        self.assertEqual(story_detail.data['created_by_user'], 'abhi')

    def test_other_user_view_story_detail(self):
        """
        Negative test
        check if appropriate error is thrown
        in case user tries to view story created by other user
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=arun' % story_id)
        self.assertEqual(story_detail.status_code, 401)
        self.assertEqual(story_detail.data, {'error': 'Unauthorized access'})

    def test_admin_view_story_detail(self):
        """
        check if admin is able to view story detail
        of story created by user
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=arun')
        story_id = stories_listing.data[0]['id']
        story_detail = test_client.get('/stories/%d?user=boss' % story_id)
        self.assertEqual(story_detail.status_code, 200)
        self.assertEqual(story_detail.data['created_by_user'], 'arun')

    def test_user_list_stories_with_status_filter(self):
        """
        check if user is able to query list of stories
        passing status filter
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=abhi&status=draft')
        self.assertEqual(len(stories_listing.data), 2)
        self.assertEqual(stories_listing.data[0]['status'], 'DRAFT')
        self.assertEqual(stories_listing.data[1]['status'], 'DRAFT')

    def test_admin_list_stories_with_status_filter(self):
        """
        check if admin is able to query list of stories
        passing status filter
        """
        test_client = self.client
        stories_listing = test_client.get('/stories?user=boss&status=draft')
        self.assertEqual(len(stories_listing.data), 4)
        self.assertEqual(stories_listing.data[2]['status'], 'DRAFT')
        self.assertEqual(stories_listing.data[3]['status'], 'DRAFT')