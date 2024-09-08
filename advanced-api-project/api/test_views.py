from django.test import TestCase
from .models import Book, Author
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase, APIClient
from django.urls import include, path, reverse
from django.contrib.auth.models import User

# Test the filtering, searching, and ordering functionalities to verify they work as intended.
# add user authentication to the tests

# Create a user for authentication
user = User.objects.get(username='admin')
user.save()

# Create an instance of APIClient
client = APIClient()

# Authenticate the client with the created user
client.force_authenticate(user=user)


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

class BookListViewTest(APITestCase, URLPatternsTestCase):
	urlpatterns = [
		path('api/', include('api.urls'))
	]
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

	def test_list_view(self):
		url = reverse('book-list')  # Ensure 'book-list' is the name of the URL pattern
		response = self.client.get('books/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 4)

	def test_detail_view(self):
		response = self.client.get(f'books/{self.book1.id}/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['title'], 'The Catcher in the Rye')

	def test_create_view(self):
		data = {
			'title': 'The Great Gatsby',
			'author': self.author1.id,
			'publication_year': '1925'
		}
		response = self.client.post('books/create/', data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(Book.objects.count(), 5)

	def test_update_view(self):
		data = {
			'title': 'The Great Gatsby',
			'author': self.author1.id,
			'publication_year': '1925'
		}
		response = self.client.put(f'books/update/{self.book1.id}/', data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Book.objects.get(id=self.book1.id).title, 'The Great Gatsby')

	def test_delete_view(self):
		response = self.client.delete(f'books/delete/{self.book1.id}/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(Book.objects.count(), 3)

