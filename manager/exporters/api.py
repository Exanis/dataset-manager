import requests
from django.shortcuts import redirect


def api_export(data, export, collection):
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
    return redirect('display_collection_exported', uuid=collection.uuid, exported=1)
