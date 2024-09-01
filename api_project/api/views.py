from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from .serializers import BookSerializer
from .models import Book

# Create your views here.


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
