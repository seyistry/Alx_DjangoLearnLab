from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value

    def create(self, validated_data):
        # Remove user from validated_data if it exists
        validated_data.pop('user', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Remove user from validated_data if it exists
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'updated_at', 'user']

    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Content must be at least 5 characters long.")
        return value

    def create(self, validated_data):
        # Remove user from validated_data if it exists
        validated_data.pop('user', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Remove user from validated_data if it exists
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
