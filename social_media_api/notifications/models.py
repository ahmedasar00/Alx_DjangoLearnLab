from django.db import models

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    verb = models.CharField(max_length=200)

    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey("target_content_type", "target_object_id")

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        if self.target:
            return f"{self.actor.username} {self.verb} your {self.target_content_type.model}"
        return f"{self.actor.username} {self.verb}"
