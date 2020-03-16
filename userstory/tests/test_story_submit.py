from rest_framework.test import APITestCase
from userstory.tests import utils

class StoryListingTests(APITestCase):
    def setUp(self):
        utils.create_users()
        test_client = self.client
        utils.create_stories(test_client)

    def test_user_submit_own_story(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=abhi' % story_id_to_submit)
        self.assertEqual(submit_story.status_code, 202)
        updated_story = test_client.get('/stories/%d?user=abhi' % story_id_to_submit)
        self.assertEqual(updated_story.data['status'], 'FOR REVIEW')

    def test_user_submit_neighbors_story(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=arun' % story_id_to_submit)
        self.assertEqual(submit_story.status_code, 401)
        self.assertEqual(submit_story.data, {'error': 'Unauthorized access'})

    def test_admin_submit_users_story(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=boss' % story_id_to_submit)
        self.assertEqual(submit_story.status_code, 401)
        self.assertEqual(submit_story.data, {'error': 'Unauthorized access'})

    def test_admin_list_stories_for_review(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=abhi' % story_id_to_submit)

        stories_for_review = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(stories_for_review.status_code, 200)
        self.assertEqual(len(stories_for_review.data), 1)
        self.assertEqual(stories_for_review.data[0]['status'], 'FOR REVIEW')

        stories_by_arun = test_client.get('/stories?user=arun&status=draft')
        story_id_to_submit = stories_by_arun.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=arun' % story_id_to_submit)

        stories_for_review = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(stories_for_review.status_code, 200)
        self.assertEqual(len(stories_for_review.data), 2)
        for i in range(len(stories_for_review.data)):
            self.assertEqual(stories_for_review.data[i]['status'], 'FOR REVIEW')

    def test_admin_approve_story(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=abhi' % story_id_to_submit)

        admin_list_stories = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(admin_list_stories.data[0]['id'], story_id_to_submit)

        approve_story = test_client.put('/stories/%d/approve?user=boss' % story_id_to_submit)
        self.assertEqual(approve_story.status_code, 202)

        approved_story = test_client.get('/stories/%d?user=abhi' % story_id_to_submit)
        self.assertEqual(approved_story.data['status'], 'APPROVED')

    def test_user_approve_story(self):
        test_client = self.client
        stories_by_abhi = test_client.get('/stories?user=abhi&status=draft')
        story_id_to_submit = stories_by_abhi.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=abhi' % story_id_to_submit)

        admin_list_stories = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(admin_list_stories.data[0]['id'], story_id_to_submit)

        approve_story = test_client.put('/stories/%d/approve?user=abhi' % story_id_to_submit)
        self.assertContains(approve_story, 'Unauthorized access', status_code=401)

    def test_admin_reject_story(self):
        test_client = self.client
        stories_by_arun = test_client.get('/stories?user=arun&status=draft')
        story_id_to_submit = stories_by_arun.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=arun' % story_id_to_submit)

        admin_list_stories = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(admin_list_stories.data[0]['id'], story_id_to_submit)

        approve_story = test_client.put('/stories/%d/reject?user=boss' % story_id_to_submit)
        self.assertEqual(approve_story.status_code, 202)

        approved_story = test_client.get('/stories/%d?user=arun' % story_id_to_submit)
        self.assertEqual(approved_story.data['status'], 'REJECTED')

    def test_user_reject_story(self):
        test_client = self.client
        stories_by_arun = test_client.get('/stories?user=arun&status=draft')
        story_id_to_submit = stories_by_arun.data[0]['id']
        submit_story = test_client.put('/stories/%d/submit?user=arun' % story_id_to_submit)

        admin_list_stories = test_client.get('/stories?user=boss&status=for%20review')
        self.assertEqual(admin_list_stories.data[0]['id'], story_id_to_submit)

        approve_story = test_client.put('/stories/%d/reject?user=arun' % story_id_to_submit)
        self.assertContains(approve_story, 'Unauthorized access', status_code=401)