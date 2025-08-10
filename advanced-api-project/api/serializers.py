from rest_framework import serializers
from .models import Author, Book
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    It includes custom validation to prevent a book from being published
    in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['author'] # The author is set when creating the book via the AuthorSerializer

    def validate_publication_year(self, value):
        """
        Custom validator to ensure the publication year is not in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value



# Serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes nested serialization for the related books.
    """

    # Serialize the related books (reverse relationship to the Book model).
    # Using 'many=True' because an author can have multiple books.
    # 'read_only=True' ensures that the books cannot be directly created/updated via this serializer.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
        # 'fields' defines the fields that will be included in the serialized output.

    """
    Notes:
    - The `books` field relies on the reverse relationship defined in the Book model.
      Ensure the `Book` model's foreign key to `Author` uses `related_name='books'`
      or leave it as default (Django will use the lowercase name of the model, i.e., 'book').
    """
