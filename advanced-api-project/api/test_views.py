from django.test import TestCase
from .models import Book, Author

# Test the filtering, searching, and ordering functionalities to verify they work as intended.


class BookFilterSearchOrderTest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='J.D. Salinger')
        self.author2 = Author.objects.create(name='Harper Lee')
        self.author3 = Author.objects.create(name='George Orwell')
        self.book1 = Book.objects.create(
            title='The Catcher in the Rye', author=self.author1, publication_year='1951')
        self.book2 = Book.objects.create(
            title='To Kill the Mockingbird', author=self.author2, publication_year='1960')
        self.book3 = Book.objects.create(
            title='1984', author=self.author3, publication_year='1949')
        self.book4 = Book.objects.create(
            title='Animal Farm', author=self.author3, publication_year='1945')

    def test_filtering(self):
        # Test filtering by publication year
        queryset = Book.objects.filter(publication_year='1949')
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].title, '1984')

    def test_searching(self):
        # Test searching by title
        queryset = Book.objects.filter(title__icontains='the')
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset[0].title, 'The Catcher in the Rye')
        self.assertEqual(queryset[1].title, 'To Kill the Mockingbird')

    def test_ordering(self):
        # Test ordering by publication year
        queryset = Book.objects.all().order_by('publication_year')
        self.assertEqual(queryset[0].title, 'Animal Farm')
        self.assertEqual(queryset[1].title, '1984')
        self.assertEqual(queryset[2].title, 'The Catcher in the Rye')
        self.assertEqual(queryset[3].title, 'To Kill the Mockingbird')
