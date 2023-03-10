from django.db import models
from django.utils import timezone

from apps.accounts.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title
