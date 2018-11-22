import requests
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
    requests.request(
        export.method,
        export.url,
        json=data,
        headers=headers,
        **params
    )
    messages.success(request, "Data exported.")
    return redirect('display_collection', uuid=collection.uuid)
