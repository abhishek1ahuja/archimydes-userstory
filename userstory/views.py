from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Story
from .serializers import *

import datetime

def check_user_validity(request):
    username = request.query_params.get('user', None)
    if username == None:
        return 1
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return 2

error_messages = {
                'user':{'1': 'specify user=<username> as a query parameter',
                        '2': 'User with this username does not exist'
                        },
                'story':{'2': 'Story with this id does not exist'
                         }
                }

def check_story_validity(story_id):
    try:
        story = Story.objects.get(pk=story_id)
        return story
    except Story.DoesNotExist:
        return 2

@api_view(['GET', 'POST'])
def stories_list(request):
    """
    List all products, or create a new product.
    """
    user = check_user_validity(request)
    if(type(user)) != User:
        return Response( {'error': error_messages['user'][user] }, status=status.HTTP_400_BAD_REQUEST )
    story_status = request.query_params.get('status', None)

    # handling retrival of stories
    if request.method == 'GET':
        if user.user_type == "admin":
            stories = Story.objects.all()
        elif user.user_type == "user":
            stories = Story.objects.filter(created_by=user.id)
        if story_status is not None:
            stories = stories.filter(status=story_status.upper())
        serializer = StoryRetrieveBriefSerializer(stories, context={'request': request}, many=True)
        return Response(serializer.data)

    # handling creation of stories
    elif request.method == 'POST':
        story = request.data
        story['created_by'] = user.id
        story['last_updated_by'] = user.id
        story['status'] = "DRAFT"
        serializer = StoryCreateSerializer(data=story)
        if serializer.is_valid():
            new_story = serializer.save()
            return Response({'id': new_story.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def story_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """

    user = check_user_validity(request)
    if (type(user)) != User:
        return Response({'error': error_messages['user'][user]}, status=status.HTTP_400_BAD_REQUEST)

    story = check_story_validity(pk)
    if type(story) != Story:
        return Response({'error': error_messages['story'][story]}, status=status.HTTP_404_NOT_FOUND)

    if not(user.user_type == "admin" or user.id == story.created_by.id):
        return Response({'error': 'Unauthorized access'},status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = StoryRetrieveSerializer(story,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        username = request.query_params.get('user', None)
        user = User.objects.get(username=username)
        if story['status'] in ['APPROVED', 'REJECTED']:
            story['status'] = 'DRAFT'
        story['last_updated_by'] = user.id
        serializer = StoryCreateSerializer(story, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all products, or create a new product.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    user = check_user_validity(request)
    if (type(user)) != User:
        return Response({'error': error_messages['user'][user]}, status=status.HTTP_404_BAD_REQUEST)

    if request.method == 'GET':
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def story_submit(request, pk):

    user = check_user_validity(request)
    if (type(user)) != User:
        return Response({'error': error_messages['user'][user]}, status=status.HTTP_400_BAD_REQUEST)

    story = check_story_validity(pk)
    if type(story) != Story:
        return Response({'error': error_messages['story'][story]}, status=status.HTTP_404_NOT_FOUND)

    if user.id == story.created_by.id:
        if story.status == 'DRAFT':
            story.status = 'FOR REVIEW'
            story.save()
            return Response({'success': 'Story %d submitted for approval' % story.id},
                            status=status.HTTP_202_ACCEPTED)
        elif story.status == 'FOR REVIEW':
            return Response({'response': 'Story %d is already submitted for approval' % story.id},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized access'},status=status.HTTP_401_UNAUTHORIZED)


def story_approve_reject(request, pk, action):

    user = check_user_validity(request)
    if (type(user)) != User:
        return Response({'error': error_messages['user'][user]}, status=status.HTTP_400_BAD_REQUEST)

    story = check_story_validity(pk)
    if type(story) != Story:
        return Response({'error': error_messages['story'][story]}, status=status.HTTP_404_NOT_FOUND)

    if user.user_type == 'admin':
        if story.status == 'FOR REVIEW':
            story.status = action.upper() + 'ED'
            story.save()
            return Response({'success': 'Story %d %sed' % (story.id, action)},
                            status=status.HTTP_202_ACCEPTED)
        elif story.status == 'APPROVED':
            return Response({'response': 'Story %d is already %sed' % (story.id, action)},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'response': 'Story %d in %s state cannot be %sed' % (story.id, story.status, action)},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized access! Only admins can approve/reject stories.'},
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def story_approve(request, pk):
    return story_approve_reject(request, pk, 'approv')

@api_view(['PUT'])
def story_reject(request, pk):
    return story_approve_reject(request, pk, 'reject')