from manager import models
from django.utils import timezone


def start_task(uuid):
    task = models.Task.objects.get(uuid=uuid)
    task.start = timezone.now()
    task.save()


def mark_task_as_done(uuid):
    task = models.Task.objects.get(uuid=uuid)
    task.end = timezone.now()
    task.save()
