from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    """
    Model representing a blog post.

    Fields:
        title (CharField): Title of the post (max length 200).
        content (TextField): The main body/content of the post.
        published_date (DateTimeField): The date and time when the post was created.
        Automatically set on creation.
        author (ForeignKey -> User): The user who created the post.
        If the user is deleted, their posts are also deleted.
    Default is user with ID=1.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    tags = TaggableManager()

    def __str__(self):
        """
        Returns the title of the post as its string representation.
        """
        return self.title


class Comment(models.Model):
    """
    Model representing a comment on a post.

    Fields:
        post (ForeignKey -> Post): The related blog post.
        If the post is deleted, its comments are also deleted.
        author (ForeignKey -> User): The user who wrote the comment.
        content (TextField): The body/content of the comment.
        created_at (DateTimeField): Date and time the comment was created.
        Automatically set on creation.
        updated_at (DateTimeField): Date and time the comment was last updated.
        Automatically updated on save.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string showing the comment's author and the related post title.
        """
        return f"Comment by {self.author} on {self.post.title}"


class Tag(models.Model):
    """
    Model representing a tag for a blog post.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Return a readable string representation of the tag.
        """
        return self.name
