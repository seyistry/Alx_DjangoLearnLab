from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .permissions import IsSelfOrReadOnly 
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification



class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),
        })

    def put(self, request):
        user = request.user
        user.bio = request.data.get('bio', user.bio)
        user.email = request.data.get('email', user.email)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        return Response({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
        })

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        user = request.user

        if user == target_user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if target_user.followers.filter(id=user.id).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Add follower relationship
        target_user.followers.add(user)

        # Create a notification for the target user
        Notification.objects.create(
            recipient=target_user,
            actor=user,
            verb="followed",
            target_content_type=ContentType.objects.get_for_model(user),
            target_object_id=user.id
        )

        return Response({"success": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Fetch all users using CustomUser.objects.all() and get the user to unfollow
        users = CustomUser.objects.all()
        user_to_unfollow = get_object_or_404(users, id=user_id)

        # Check if the current user is following this user
        if user_to_unfollow in request.user.following.all():
            request.user.following.remove(user_to_unfollow)
            return Response({"success": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        
        return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
