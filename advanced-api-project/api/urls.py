from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookViewSet,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

router = DefaultRouter()


router.register(r'authors', AuthorViewSet)  
router.register(r'books', BookViewSet, basename='books')  

urlpatterns = [

    path('', include(router.urls)),


    path('books/list/', BookListView.as_view(), name='book-list'), 
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), 
    path('books/create/', BookCreateView.as_view(), name='book-create'), 
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  
]
