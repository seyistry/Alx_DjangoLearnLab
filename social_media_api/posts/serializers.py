from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # Ensure that the user who created the post is the one who is authenticated
    def validate(self, data):
        user = self.context['request'].user
        data['user'] = user
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    # Ensure that the user who created the comment is the one who is authenticated
    def validate(self, data):
        user = self.context['request'].user
        data['user'] = user
        return data