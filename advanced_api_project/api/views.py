from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Author models,
    including create, list, retrieve, update, and destroy.
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on the Book model.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
