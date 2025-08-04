from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",  # Allows reverse lookup: author.books.all()
    )

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ["title"]


class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book,
        related_name="libraries",  # Allows reverse lookup: book.libraries.all()
        blank=True,  # A library can exist without books
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Libraries"


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name="librarian",  # Allows reverse lookup: library.librarian
    )

    def __str__(self):
        return f"{self.name} (Librarian of {self.library.name})"

    class Meta:
        ordering = ["name"]


##########################
class UserRegisterView(CreateView):
    # Use Django's built-in form for creating a user
    form_class = UserCreationForm
    # Redirect to the login page after successful registration
    success_url = reverse_lazy("login")
    # Specify the template for the registration form
    template_name = "relationship_app/register.html"

    def get(self, request, *args, **kwargs):
        # Render the registration form
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handle form submission for registration
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)




###########################


#! Access Control in Django


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    def __str__(self):
        """String representation of the UserProfile object."""

        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        role = (
            UserProfile.Role.ADMIN if instance.is_superuser else UserProfile.Role.MEMBER
        )
        UserProfile.objects.create(user=instance, role=role)

    instance.userprofile.save()
