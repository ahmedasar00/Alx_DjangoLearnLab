from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters 
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from rest_framework import filters
from .serializers import BookSerializer
from .filters import BookFilter

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Author models,
    including create, list, retrieve, update, and destroy.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
 

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on the Book model.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer







class BookListView(generics.ListAPIView):
    """
    API endpoint to retrieve a list of all Book instances.
    - HTTP Method: GET
    - Permissions: Allow any user (authenticated or not) to access.
    - Response: Returns a serialized list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    
  
    """
    Filtering, Searching, and Ordering Configuration:
    filter_backends: Activates the necessary backends for filtering (DjangoFilterBackend), searching (SearchFilter), and ordering (OrderingFilter).
    filterset_fields: Allows for precise filtering on the 'title', 'author', and 'publication_year' fields.
    search_fields: Enables full-text search capabilities on the 'title' and 'author' fields using the search parameter.
    ordering_fields: Permits clients to sort the results by 'title' or 'publication_year' using the ordering parameter.
    """ 
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]  
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author'] 
    ordering_fields = ['title', 'publication_year']

    






class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve details of a single Book by its primary key (pk).
    - HTTP Method: GET
    - Permissions: Allow any user to access.
    - URL Params: pk (primary key of the book)
    - Response: Returns serialized data of the specified book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new Book instance.
    - HTTP Method: POST
    - Permissions: Only authenticated users can create.
    - Request Body: Expects data according to BookSerializer.
    - Response: Returns the serialized newly created book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]





class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update an existing Book instance.
    - HTTP Methods: PUT, PATCH
    - Permissions: Only authenticated users can update.
    - URL Params: pk (primary key of the book to update)
    - Request Body: Expects partial or full update data as per BookSerializer.
    - Response: Returns the serialized updated book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete an existing Book instance.
    - HTTP Method: DELETE
    - Permissions: Only authenticated users can delete.
    - URL Params: pk (primary key of the book to delete)
    - Response: Returns HTTP 204 No Content on successful deletion.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]