from rest_framework import serializers
from userstory.models import User, Story

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('summary', 'description', 'story_type', 'complexity', 'estimated_time', 'cost', 'created_by')

class StoryRetrieveSerializer(serializers.ModelSerializer):
    created_by_user = serializers.CharField(source='created_by.username')
    updated_by_user = serializers.CharField(source='last_updated_by.username')

    class Meta:
        model = Story
        fields = ("id", "summary", "description", "story_type", "complexity", "estimated_time",
                  "cost", "status", "created_at", "created_by_user",
                  "last_updated_at", "updated_by_user")

class StoryRetrieveBriefSerializer(serializers.ModelSerializer):
    created_by_user = serializers.CharField(source='created_by.username')
    updated_by_user = serializers.CharField(source='last_updated_by.username')

    class Meta:
        model = Story
        fields = ("id", "summary", "story_type", "status",
                  "created_at", "created_by_user",
                  "last_updated_at", "updated_by_user")