from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    is_read = models.BooleanField(default=False)

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor_notifications')
    # E.g., "liked", "commented on", "followed"
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Generic relation to the target object (e.g., Post, Comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')

    class Meta:
        ordering = ['-timestamp']

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f'{self.actor} {self.verb} {self.target}'
