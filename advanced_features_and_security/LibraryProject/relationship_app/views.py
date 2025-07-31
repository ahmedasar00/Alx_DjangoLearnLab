from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Book, Library
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView


def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in directly after registration
            login(request, user)
            return redirect(
                "relationship_app:list_books"
            )  # Redirect to book list after registration
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "relationship_app:list_books"
                )  # Redirect to book list after login
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"


class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


def is_admin(user):
    return user.is_authenticated and user.userprofile.role == "ADMIN"


def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == "LIBRARIAN"


def is_member(user):
    return user.is_authenticated and user.userprofile.role == "MEMBER"


@login_required
@user_passes_test(is_admin, login_url="/")
def admin_view(request):
    return render(request, "admin_view.html")


@login_required
@user_passes_test(is_librarian, login_url="/")
def librarian_view(request):
    return render(request, "librarian_view.html")


@login_required
@user_passes_test(is_member, login_url="/")
def member_view(request):
    return render(request, "member_view.html")
