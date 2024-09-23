from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions, serializers, status, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification  # Import the Notification model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Content must be at least 10 characters long.")
        return value

    # Ensure that the user who created the post is the one who is authenticated
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete this post")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'updated_at', 'user']

    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Content must be at least 5 characters long.")
        return value

    # Ensure that the user who created the comment is the one who is authenticated
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete this comment")
        instance.delete()


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the users the current user is following
        following_users = request.user.following.all()

        # Get posts by followed users and order by creation date (most recent first)
        posts = Post.objects.filter(
            author__in=following_users).order_by('-created_at')

        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    # "Like.objects.get_or_create(user=request.user, post=post)"]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        # Check if the user has already liked this post
        if Like.objects.filter(post=post, user=user).exists():
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new like
        Like.objects.create(post=post, user=user)

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )

        return Response({"success": "Post liked."}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user

        # Check if the user has liked this post
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"success": "Post unliked."}, status=status.HTTP_200_OK)

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user
        content = request.data.get("content")

        # Create the comment
        comment = Comment.objects.create(post=post, author=user, content=content)

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="commented on",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )

        return Response({"success": "Comment added."}, status=status.HTTP_201_CREATED)
