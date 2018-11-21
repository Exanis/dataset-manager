from django.contrib import messages
from django.shortcuts import redirect
from manager import models, tasks


def api_export(data, export, collection, request):
    params = {}
    if export.username != '':
        params['auth'] = (export.username, export.password)
    headers = {
        'Content-type': 'application/json'
    }
    for header in export.params:
        headers[header.name] = header.value
    task = models.Task.objects.create(
        name='Export ' + collection.name + ' using ' + export.name
    )
    tasks.api_export.delay(task.uuid, export.method, export.url, params, data, headers)
    messages.success(request, "Export started.")
    return redirect('display_collection', uuid=collection.uuid)
