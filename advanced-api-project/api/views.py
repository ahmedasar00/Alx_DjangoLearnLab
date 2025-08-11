from rest_framework import viewsets, generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Book models.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
 

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on the Author model.
    (Corrected to use Author model and serializer)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    API endpoint to retrieve a list of all Book instances with filtering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # This list activates the filtering, searching, and ordering features
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Configure fields for each feature
    filterset_fields = ['title', 'author', 'publication_year'] # For ?publication_year=2024
    search_fields = ['title', 'author'] # For ?search=query
    ordering_fields = ['title', 'publication_year'] # For ?ordering=title


class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve details of a single Book by its primary key (pk).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update an existing Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete an existing Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]