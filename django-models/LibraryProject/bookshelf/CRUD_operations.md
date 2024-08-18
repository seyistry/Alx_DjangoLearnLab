```
>>> from bookshelf.models import Book
>>> new_book = Book.objects.create(
    title="1984",
    author=“George Orwell”,
    publication_year=1949,
)
>>> Book.objects.get(title="1984")
{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}
>>> update_book = Book.objects.get(id=1)
>>> update_book.title = "Nineteen Eighty-Four"
>>> update_book.save()
>>> books = Book.objects.all().values().first()
>>> print(books)
{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}
>>> update_book.delete()
(1, {'bookshelf.Book': 1})
>>> books = Book.objects.all().values().first()
>>> print(books)
None
>>> 
```