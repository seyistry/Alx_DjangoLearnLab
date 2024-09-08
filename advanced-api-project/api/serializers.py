from rest_framework import serializers
from .models import Book, Author


from datetime import datetime

# This is the serializer for the Book model
# It has a Meta class that specifies the model and the fields to include in the serialization
# The validate method is used to validate the publication year field
# If the publication year is in the future, a validation error is raised
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        if data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError(
                "Publication year must be in the future")
        return data

# This is the serializer for the Author model
# It has a Meta class that specifies the model and the fields to include in the serialization
# The book field is a nested serializer that includes the BookSerializer
# This allows the books associated with an author to be included in the serialization
# The AuthorSerializer is used in the views to serialize author objects
class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'book']
