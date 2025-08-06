from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token


# Step 2: Set Up a Router
# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")


urlpatterns = [
    path("books/", BookList.as_view(), name="book-list"),
    #    Include the router URLs for BookViewSet (all CRUD operations)
    path(
        "", include(router.urls)
    ),  # This includes all routes registered with the router
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
