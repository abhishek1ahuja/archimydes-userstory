from userstory.models import *

def create_users():
    abhi = User(name='abhishek', username='abhi', user_type='user')
    arun = User(name='arunkumar', username='arun', user_type='user')
    boss = User(name='sivaji', username='boss', user_type='admin')
    abhi.save()
    arun.save()
    boss.save()


def make_story(summary, story_type):
    return {'summary': summary,
            'description': 'desc',
            'complexity': '3',
            'estimated_time': '04:00:00',
            'cost': '6',
            'story_type': story_type}

def create_stories(test_client):
    test_client.post('/stories?user=abhi', data=make_story('sample story 1', 'testing'), format='json')
    test_client.post('/stories?user=abhi', data=make_story('sample story 2', 'testing'), format='json')
    test_client.post('/stories?user=arun', data=make_story('sample story 11', 'testing'), format='json')
    test_client.post('/stories?user=arun', data=make_story('sample story 12', 'testing'), format='json')