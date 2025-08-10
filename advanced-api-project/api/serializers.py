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




class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    This serializer uses a nested BookSerializer to handle the 'books'
    related field. This means that when you retrieve an author, the response
    will include a list of all their books. When creating or updating an
    author, you can also create or update their books in the same request.
    
    The 'books' field is read_only to prevent accidental removal of
    books when updating the author, but it can be used for nested creation.
    We'll override the create and update methods to handle this.
    """
    books = BookSerializer(many=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    def create(self, validated_data):
        """
        Override the create method to handle nested books.
        It first creates the author and then iterates through the books data
        to create each book, linking it to the newly created author.
        """
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        return author
    
    def update(self, instance, validated_data):
        """
        Override the update method to handle nested books.
        It updates the author's name and then handles books. This
        implementation assumes you are adding new books to an existing author.
        For more complex logic (updating existing books or deleting them),
        you would need additional steps.
        """
        books_data = validated_data.pop('books', [])

        instance.name = validated_data.get('name', instance.name)
        instance.save()

        for book_data in books_data:
            Book.objects.create(author=instance, **book_data)
        
        return instance
