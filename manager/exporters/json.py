import json
import io
from django.http.response import FileResponse


def json_export(data, export, collection, request):
    content = json.dumps(data)
    pseudo_file = io.BytesIO(str.encode(content))
    return FileResponse(
        pseudo_file,
        filename=collection.name + ".json",
        as_attachment=True
    )
