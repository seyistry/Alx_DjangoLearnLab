from django.db import models

# Create your models here.

# this is the model for the Author
# it has a name field
# the __str__ method is used to return the name of the author when the object is printed
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# this is the model for the Book
# it has a title field, an author field which is a foreign key to the Author model
# and a publication_year field
# the __str__ method is used to return the title of the book when the object is printed
# the Author model is imported at the top of this file
# the on_delete argument is set to CASCADE which means that if an author is deleted, all the books associated with that author will also be deleted
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
