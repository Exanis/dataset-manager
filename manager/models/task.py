from uuid import uuid4
from django.utils import timezone
from django.db import models


class Task(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    registered = models.DateTimeField(default=timezone.now)
    start = models.DateTimeField(null=True, default=None)
    end = models.DateTimeField(null=True, default=None)
    
    class Meta():
        ordering = ['-end', '-start', 'registered']
