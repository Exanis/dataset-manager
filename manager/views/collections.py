from random import randint
from django.shortcuts import render, redirect, get_object_or_404
from manager import models, generators, validators


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


def _make_visible_list(target_type, include_all=False, prefix='', forbidden=None):
    result = []
    if forbidden is None:
        forbidden = []
    if target_type in forbidden:
        return result
    for field in target_type.fields:
        if field.recap or include_all:
            if field.data_type.data_type == 'struct':
                result = result + _make_visible_list(
                    field.data_type,
                    include_all,
                    field.name + ' > ',
                    [target_type] + forbidden
                )
            else:
                result.append({
                    'name': prefix + field.name,
                    'field': field
                })
    return result


def items(request, uuid, exported=0):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    return render(
        request,
        'collections/collection.html', {
            'exported': exported == 1,
            'visible': _make_visible_list(collection.type),
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


def items_value(request, uuid):
    obj = get_object_or_404(models.CollectionElement, uuid=uuid)
    return render(
        request,
        'collections/item.html',
        {
            'exported': False,
            'visible': _make_visible_list(obj.collection.type),
            'exports': models.Export.objects.all(),
            'fields': _make_visible_list(obj.collection.type, include_all=True),
            'collection': obj.collection,
            'collections': models.Collection.objects.all(),
            'item': obj,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def items_value_add(request, uuid):
    parent = get_object_or_404(models.CollectionElement, uuid=uuid)
    data_type = get_object_or_404(models.DataTypeElement, uuid=request.POST['type'])
    obj = models.CollectionElementValue.objects.create(
        element=parent,
        key=data_type,
        value=request.POST['value']
    )
    return redirect('display_value', uuid=parent.uuid)


def items_value_del(request, uuid):
    obj = get_object_or_404(models.CollectionElementValue, uuid=uuid)
    target = obj.element.uuid
    obj.delete()
    return redirect('display_value', uuid=target)


def _generate(item, field, count):
    gen = getattr(generators, field.data_type.data_type + "_generator")
    cnt = len(item.values_for(field))
    for _ in range(count):
        value = gen(field.data_type, cnt)
        cnt += 1
        models.CollectionElementValue.objects.create(
            element=item,
            key=field,
            value=value
        )


def items_value_generate(request, item_uuid, field_uuid):
    item = get_object_or_404(models.CollectionElement, uuid=item_uuid)
    field = get_object_or_404(models.DataTypeElement, uuid=field_uuid)
    _generate(item, field, int(request.POST['count']))
    return redirect('display_value', uuid=item.uuid)


def collection_items_generate_selection(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    fields = _make_visible_list(collection.type, include_all=True)
    needed_fields = [f for f in fields if f['field'].data_type.fixed]
    return render(
        request,
        'collections/generate.html', {
            'fix': False,
            'exported': False,
            'visible': _make_visible_list(collection.type),
            'exports': models.Export.objects.all(),
            'needed': needed_fields,
            'collection': collection,
            'collections': models.Collection.objects.all(),
            'item': None,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def collection_items_generate(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    generate_count = int(request.POST['count'])
    fields = _make_visible_list(collection.type, include_all=True)
    for _ in range(generate_count):
        item = models.CollectionElement.objects.create(collection=collection)
        for field_base in fields:
            field = field_base['field']
            count = randint(field.min_count, field.max_count)
            if str(field.uuid) + '-fixed' in request.POST:
                for __ in range(count):
                    models.CollectionElementValue.objects.create(
                        element=item,
                        key=field,
                        value=request.POST[str(field.uuid)]
                    )
            else:
                _generate(item, field, count)
    return redirect('display_collection', uuid=collection.uuid)


def collection_fix(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    fields = _make_visible_list(collection.type, include_all=True)
    needed_fields = [f for f in fields if f['field'].data_type.fixed]
    return render(
        request,
        'collections/generate.html', {
            'fix': True,
            'exported': False,
            'visible': _make_visible_list(collection.type),
            'exports': models.Export.objects.all(),
            'needed': needed_fields,
            'collection': collection,
            'collections': models.Collection.objects.all(),
            'item': None,
            'types': models.DataType.objects.filter(data_type='struct')
        }
    )


def collection_items_generate_fix(request, uuid):
    collection = get_object_or_404(models.Collection, uuid=uuid)
    fields = _make_visible_list(collection.type, include_all=True)
    enforce = 'enforce' in request.POST
    generate_all = 'all' in request.POST
    for item in collection.elements:
        for field_base in fields:
            field = field_base['field']
            if str(field.uuid) + '-fixed' in request.POST and enforce:
                item.values_for(field).delete()
                count = randint(field.min_count, field.max_count)
                for _ in range(count):
                    models.CollectionElementValue.objects.create(
                        element=item,
                        key=field,
                        value=request.POST[str(field.uuid)]
                    )
            else:
                if generate_all or not item.is_field_valid(field):
                    validator = getattr(validators, field.data_type.data_type + '_validator')
                    values = item.values_for(field)
                    existing = len(values)
                    for value in values:
                        if generate_all or not validator(value.value, field.data_type):
                            value.delete()
                            existing -= 1
                    count = randint(field.min_count - existing, field.max_count - existing)
                    if str(field.uuid) + '-fixed' in request.POST:
                        for _ in range(count):
                            models.CollectionElementValue.objects.create(
                                element=item,
                                key=field,
                                value=request.POST[str(field.uuid)]
                            )
                    else:
                        _generate(item, field, count)
    return redirect('display_collection', uuid=collection.uuid)


def collection_duplicate(request, uuid):
    old_collection = get_object_or_404(models.Collection, uuid=uuid)
    collection = models.Collection.objects.create(
        name=request.POST['name'],
        type=old_collection.type
    )
    for old_item in old_collection.elements:
        item = models.CollectionElement.objects.create(
            order=old_item.order,
            collection=collection
        )
        for old_value in old_item.values:
            models.CollectionElementValue.objects.create(
                element=item,
                value=old_value.value,
                key=old_value.key,
                order=old_value.order
            )
    return redirect('display_collection', uuid=collection.uuid)
