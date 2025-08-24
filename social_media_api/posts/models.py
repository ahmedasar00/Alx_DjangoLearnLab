from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=230)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.title


class Commment(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    title = models.CharField(max_length=230)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.Post.title}"
