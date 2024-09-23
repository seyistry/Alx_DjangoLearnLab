from rest_framework import status, generics
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
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def post(self, request, username):
        # Get the user to follow
        user_to_follow = get_object_or_404(CustomUser, username=username)
        
        # Ensure the user is not trying to follow themselves
        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the user to the following list if not already followed
        if user_to_follow not in request.user.following.all():
            request.user.following.add(user_to_follow)
            return Response({"success": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        
        return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def post(self, request, username):
        # Get the user to unfollow
        user_to_unfollow = get_object_or_404(CustomUser, username=username)

        # Check if the current user is following this user
        if user_to_unfollow in request.user.following.all():
            request.user.following.remove(user_to_unfollow)
            return Response({"success": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        
        return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
