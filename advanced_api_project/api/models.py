from django.db import models


class Author(models.Model):
    """
    Model to store author information. The 'name' field is a string
    to store the author's full name. This model forms a one-to-many
    relationship with the Book model, meaning one author can have
    multiple books.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model to store book information.
    - 'title' is a string field for the book's title.
    - 'publication_year' is an integer for the year of publication.
    - 'author' is a ForeignKey that links to the Author model.
      This establishes the one-to-many relationship. `on_delete=models.CASCADE`
      ensures that if an author is deleted, all of their books are also deleted.
      `related_name='books'` allows us to easily access a list of an author's
      books from the Author model instance (e.g., `author_instance.books.all()`).
    """

    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author.name}"
