from rest_framework import serializers
from .models import (
    Book,
    Author
)


class BookSerializer(serializers.models):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.models):
	class Meta:
		model = Author
		fields = '__all__'
