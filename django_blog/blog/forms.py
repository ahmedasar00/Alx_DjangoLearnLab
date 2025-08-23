from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form extending Django's built-in UserCreationForm.

    Adds an email field and ensures it is saved along with the user account.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """
        Saves the user instance with the email field.

        Args:
            commit (bool): Whether to save the user immediately to the database.

        Returns:
            User: The created User instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    """
    Form for creating or updating a blog post.
    Maps to the Post model with title and content fields.
    """

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {"tags": TagWidget()}


class CommentForm(forms.ModelForm):
    """
    Form for creating or updating a comment.
    Maps to the Comment model with a single content field.
    Includes a widget for better text area display.
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }


class SearchForm(forms.Form):
    """
    A simple form for handling search queries.
    """

    query = forms.CharField(
        label="Search",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Search posts..."}),
    )
