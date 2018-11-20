from django.shortcuts import redirect, render, get_object_or_404
from manager import models, formats, exporters, tasks


def exports(request):
    return render(
        request,
        'exports/index.html',
        {
            'export': None,
            'exports': models.Export.objects.all()
        }
    )


def exports_add(request):
    obj = models.Export.objects.create(
        name=request.POST['name']
    )
    return redirect('display_export', uuid=obj.uuid)


def exports_del(request, uuid):
    obj = get_object_or_404(models.Export, uuid=uuid)
    obj.delete()
    return redirect('index_export')


def exports_view(request, uuid):
    export = get_object_or_404(models.Export, uuid=uuid)
    return render(
        request,
        'exports/details.html',
        {
            'export': export,
            'exports': models.Export.objects.all()
        }
    )


def exports_update(request, uuid):
    export = get_object_or_404(models.Export, uuid=uuid)
    export.type = request.POST['type']
    if 'username' in request.POST:
        export.username = request.POST['username']
    if 'password' in request.POST:
        export.password = request.POST['password']
    if 'url' in request.POST:
        export.url = request.POST['url']
    if 'method' in request.POST:
        export.resource = request.POST['method']
    export.flatten = 'flatten' in request.POST
    export.save()
    return redirect('display_export', uuid=export.uuid)


def exports_param_add(request, uuid):
    export = get_object_or_404(models.Export, uuid=uuid)
    models.ExportParam.objects.create(
        export=export,
        name=request.POST['name'],
        value=request.POST['value']
    )
    return redirect('display_export', uuid=export.uuid)


def exports_param_del(request, uuid):
    obj = get_object_or_404(models.ExportParam, uuid=uuid)
    target = obj.export
    obj.delete()
    return redirect('display_export', uuid=target.uuid)


def _retrieve_object(t, obj, flatten, ignore_not_flat):
    result = {}
    for field in t.fields:
        if field.data_type.data_type == 'struct':
            if ignore_not_flat and not flatten:
                continue
            sub_object = _retrieve_object(field.data_type, obj, flatten, False)
            if flatten:
                result.update(sub_object)
            else:
                result[field.name] = sub_object
        else:
            formatter = getattr(formats, field.data_type.data_type + '_format')
            if field.max_count == 1:
                val = obj.values_for(field)
                if len(val) == 1:
                    result[field.name] = formatter(val[0].value)
            else:
                val = obj.values_for(field)
                result[field.name] = [formatter(v.value) for v in val]
    return result


def export_collection(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    export = get_object_or_404(models.Export, uuid=request.POST['export'])
    result = []
    for item in collection.elements:
        if item.is_valid:
            result.append(
                _retrieve_object(
                    collection.type,
                    item,
                    export.flatten,
                    export.type == 'db'
                )
            )
    exporter = getattr(exporters, export.type + '_export')
    return exporter(result, export, collection)


def export_duplicate(request, uuid):
    tasks.duplicate_export.delay(uuid, request.POST['name'])
    return redirect('index_export')
