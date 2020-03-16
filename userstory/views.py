from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Story
from .serializers import *

import datetime

@api_view(['GET', 'POST'])
def stories_list(request):
    """
    List all products, or create a new product.
    """
    username = request.query_params.get('user', None)
    story_status = request.query_params.get('status', None)
    if username == None:
        return Response({'error':'specify user=<username> as a query parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        if request.method == 'GET':
            if user.user_type == "admin":
                stories = Story.objects.all()
            elif user.user_type == "user":
                stories = Story.objects.filter(created_by=user.id)
            if story_status is not None:
                stories = stories.filter(status=story_status.upper())
            serializer = StoryRetrieveBriefSerializer(stories, context={'request': request}, many=True)
            return Response(serializer.data)
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
    except User.DoesNotExist as err:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def story_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    username = request.query_params.get('user', None)
    if username == None:
        return Response({'error':'specify user=<username> as a query parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        try:
            story = Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not(user.user_type == "admin" or user.id == story.created_by.id):
            return Response({'error': 'Unauthorized access'},status=status.HTTP_401_UNAUTHORIZED)

        if request.method == 'GET':
            serializer = StoryRetrieveSerializer(story,context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            username = request.query_params.get('user', None)
            user = User.objects.get(username=username)
            story['last_updated_by'] = user.id
            serializer = StoryCreateSerializer(story, data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            story.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist as err:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    username = request.query_params.get('user', None)
    if username == None:
        return Response({'error': 'specify user=<username> as a query parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['PUT'])
def story_approve(request, pk):
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    username = request.query_params.get('user', None)
    if username == None:
        return Response({'error': 'specify user=<username> as a query parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.user_type == 'admin':
        if story.status == 'FOR REVIEW':
            story.status = 'APPROVED'
            story.save()
            return Response({'success': 'Story %d approved' % story.id},
                            status=status.HTTP_202_ACCEPTED)
        elif story.status == 'APPROVED':
            return Response({'response': 'Story %d is already approved' % story.id},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'response': 'Story %d in %s state cannot be approved' % (story.id, story.status)},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized access! Only admins can approve stories.'},
                        status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def story_reject(request, pk):
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    username = request.query_params.get('user', None)
    if username == None:
        return Response({'error': 'specify user=<username> as a query parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.user_type == 'admin':
        if story.status == 'FOR REVIEW':
            story.status = 'REJECTED'
            story.save()
            return Response({'success': 'Story %d rejected' % story.id},
                            status=status.HTTP_202_ACCEPTED)
        elif story.status == 'REJECTED':
            return Response({'response': 'Story %d is already rejected' % story.id},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'response': 'Story %d in %s state cannot be rejected' % (story.id, story.status)},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized access! Only admins can reject stories.'},
                        status=status.HTTP_401_UNAUTHORIZED)
