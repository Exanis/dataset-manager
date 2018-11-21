from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.transaction import atomic
from manager import models, tasks


def collections(request):
    return render(request, 'collections/index.html', {
        'collection': None,
        'collections': models.Collection.objects.all(),
        'types': models.DataType.objects.filter(data_type='struct')
    })


def collections_add(request):
    data_type = get_object_or_404(models.DataType, uuid=request.POST['type'])
    obj = models.Collection.objects.create(
        name=request.POST['name'],
        type=data_type
    )
    return redirect('display_collection', uuid=obj.uuid)


def collections_delete(request, uuid):
    target = get_object_or_404(models.Collection, uuid=uuid)
    target.delete()
    return redirect('home')


def collections_edit(request, uuid):
    target = get_object_or_404(models.Collection, uuid=uuid)
    target.name = request.POST['name']
    target.save()
    return redirect('display_collection', uuid=target.uuid)


@atomic
def items(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    return render(
        request,
        'collections/collection.html', {
            'visible': tasks.make_visible_list(collection.type),
            'exports': models.Export.objects.all(),
            'collection': collection,
            'collections': models.Collection.objects.all(),
            'item': None,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def items_add(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    obj = models.CollectionElement.objects.create(collection=collection)
    return redirect('display_value', uuid=obj.uuid)


def items_delete(request, uuid):
    obj = get_object_or_404(models.CollectionElement, uuid=uuid)
    target = obj.collection.uuid
    obj.delete()
    return redirect('display_collection', uuid=target)


@atomic
def items_value(request, uuid):
    obj = get_object_or_404(models.CollectionElement, uuid=uuid)
    return render(
        request,
        'collections/item.html',
        {
            'visible': tasks.make_visible_list(obj.collection.type),
            'exports': models.Export.objects.all(),
            'fields': tasks.make_visible_list(obj.collection.type, include_all=True),
            'collection': obj.collection,
            'collections': models.Collection.objects.all(),
            'item': obj,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


@atomic
def items_value_add(request, uuid):
    parent = get_object_or_404(models.CollectionElement, uuid=uuid)
    data_type = get_object_or_404(models.DataTypeElement, uuid=request.POST['type'])
    val = request.POST['value']
    if data_type.data_type.data_type in ['datetime', 'time']:
        timeval = val.split('T')
        timepart = timeval[1] if len(timeval) == 2 else timeval[0]
        datepart = timeval[0] + 'T' if len(timeval) == 2 else ''
        if len(timepart) == 5:
            timepart += ':00'
        val = datepart + timepart
    models.CollectionElementValue.objects.create(
        element=parent,
        key=data_type,
        value=val
    )
    return redirect('display_value', uuid=parent.uuid)


def items_value_del(request, uuid):
    obj = get_object_or_404(models.CollectionElementValue, uuid=uuid)
    target = obj.element.uuid
    obj.delete()
    return redirect('display_value', uuid=target)


@atomic
def items_value_generate(request, item_uuid, field_uuid):
    item = get_object_or_404(models.CollectionElement, uuid=item_uuid)
    field = get_object_or_404(models.DataTypeElement, uuid=field_uuid)
    tasks.generate(item, field, int(request.POST['count']))
    return redirect('display_value', uuid=item.uuid)


@atomic
def collection_items_generate_selection(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    fields = tasks.make_visible_list(collection.type, include_all=True)
    needed_fields = [f for f in fields if f['field'].data_type.fixed]
    return render(
        request,
        'collections/generate.html', {
            'fix': False,
            'visible': tasks.make_visible_list(collection.type),
            'exports': models.Export.objects.all(),
            'needed': needed_fields,
            'collection': collection,
            'collections': models.Collection.objects.all(),
            'item': None,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def collection_items_generate(request, uuid):
    formatted = {
        key: request.POST[key] for key in request.POST
    }
    collection = get_object_or_404(models.Collection, uuid=uuid)
    task = models.Task.objects.create(
        name='Generate ' + request.POST['count'] + ' items for collection ' + collection.name
    )
    tasks.generate_collection.delay(task.uuid, uuid, formatted)
    messages.success(request, 'Generation task planned.')
    return redirect('display_collection', uuid=uuid)


@atomic
def collection_fix(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    fields = tasks.make_visible_list(collection.type, include_all=True)
    needed_fields = [f for f in fields if f['field'].data_type.fixed]
    return render(
        request,
        'collections/generate.html', {
            'fix': True,
            'visible': tasks.make_visible_list(collection.type),
            'exports': models.Export.objects.all(),
            'needed': needed_fields,
            'collection': collection,
            'collections': models.Collection.objects.all(),
            'item': None,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def collection_items_generate_fix(request, uuid):
    formatted = {
        key: request.POST[key] for key in request.POST
    }
    collection = get_object_or_404(models.Collection, uuid=uuid)
    task = models.Task.objects.create(
        name='Fixing schema for collection ' + collection.name
    )
    tasks.fix_collection.delay(task.uuid, uuid, formatted)
    messages.success(request, 'Collection fix task planned.')
    return redirect('display_collection', uuid=uuid)


def collection_duplicate(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    task = models.Task.objects.create(
        name='Duplicating collection ' + collection.name
    )
    tasks.duplicate_collection.delay(task.uuid, uuid, request.POST['name'])
    messages.success(request, 'Collection duplication planned.')
    return redirect('home')
