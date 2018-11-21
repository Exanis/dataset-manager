from django.shortcuts import render
from manager import models


def tasks(request):
    return render(
        request,
        'tasks/index.html',
        {
            'done': models.Task.objects.exclude(end__isnull=True),
            'started': models.Task.objects.filter(end__isnull=True).exclude(start__isnull=True),
            'waiting': models.Task.objects.filter(start__isnull=True)
        }
    )
