from rest_framework import serializers
from .models import Book, Author


from datetime import datetime


class BookSerializer(serializers.models):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        if data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError(
                "Publication year must be in the future")
        return data


class AuthorSerializer(serializers.models):
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'book']
