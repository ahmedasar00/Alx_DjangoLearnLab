from django.urls import path
from . import views

app_name = "relationship_app"

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
 
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-dashboard/", views.admin_view, name="admin_view"),
    path("librarian-dashboard/", views.librarian_view, name="librarian_view"),
    path("member-dashboard/", views.member_view, name="member_view"),
]
