from random import randint
from celery import shared_task
from manager import models, validators, generators
from .utils import mark_task_as_done, start_task


def generate(item, field, count, parent, cnt=None):
    gen = getattr(generators, field.data_type.data_type + "_generator")
    if cnt is None:
        cnt = len(item.values_for(field))
    for _ in range(count):
        value = gen(field.data_type, cnt)
        cnt += 1
        models.CollectionElementValue.objects.create(
            element=item,
            key=field,
            value=value,
            parent=parent
        )


def make_visible_list(target_type, include_all=False, prefix='', forbidden=None, parent=None):
    result = []
    if forbidden is None:
        forbidden = []
    if target_type in forbidden:
        return result
    for field in target_type.fields:
        if field.recap or include_all:
            if field.data_type.data_type == 'struct':
                result.append({
                    'name': prefix + field.name,
                    'field': field,
                    'parent': parent
                })
                result = result + make_visible_list(
                    field.data_type,
                    include_all,
                    field.name + ' > ',
                    [target_type] + forbidden,
                    field
                )
            else:
                result.append({
                    'name': prefix + field.name,
                    'field': field,
                    'parent': parent
                })
    return result


def generate_inner_struct_data(data_type, item, request, parent, incomplete_only=False):
    for field in data_type.fields:
        if incomplete_only:
            existing_cnt = item.values_for(field)
            if field.min_count <= existing_cnt <= field.max_count:
                continue
        else:
            existing_cnt = 0
        count = randint(field.min_count - existing_cnt, field.max_count - existing_cnt)
        if field.data_type.data_type == 'struct':
            for rank in range(count):
                value = models.CollectionElementValue.objects.create(
                    element=item,
                    key=field,
                    value=generators.struct_generator(field, rank),
                    parent=parent
                )
            collections = item.values_for(field)
            for collection in collections:
                generate_inner_struct_data(field.data_type, item, request, collection, incomplete_only)
        else:
            if str(field.uuid) + 'fixed' in request:
                val = request[str(field.uuid)]
                if field.data_type.data_type in ['datetime', 'time']:
                    timeval = val.split('T')
                    timepart = timeval[1] if len(timeval) == 2 else timeval[0]
                    datepart = timeval[0] + 'T' if len(timeval) == 2 else ''
                    if len(timepart) == 5:
                        timepart += ':00'
                    val = datepart + timepart
                    for _ in range(count):
                        models.CollectionElementValue.objects.create(
                            element=item,
                            key=field,
                            value=val,
                            parent=parent
                        )
            else:
                generate(item, field, count, parent)


def generate_collection_elements(collection, generate_count, request):
    for _ in range(generate_count):
        item = models.CollectionElement.objects.create(collection=collection)
        generate_inner_struct_data(collection.type, item, request, None)


@shared_task
def generate_collection(task, uuid, request):
    start_task(task)
    collection = models.Collection.objects.get(uuid=uuid)
    generate_count = int(request['count'])
    generate_collection_elements(collection, generate_count, request)
    mark_task_as_done(task)


def clean_item(data_type, item):
    for field in data_type.fields:
        values = item.values_for(field)
        validator = getattr(validators, field.data_type.data_type + '_validator')
        for val in values:
            if not validator(field.data_type, val.value):
                val.delete()
        values = item.values_for(field)
        if len(values) > field.max_count:
            cnt = 0
            for val in values:
                cnt += 1
                if cnt > field.max_count:
                    val.delete()
        if field.data_type.data_type == 'struct':
            clean_item(field.data_type, item)


@shared_task
def fix_collection(task, uuid, request):
    start_task(task)
    collection = models.Collection.objects.get(uuid=uuid)
    if 'all' in request:
        cnt = len(collection.elements)
        collection.elements.delete()
        generate_collection_elements(collection, cnt, request)
    else:
        for item in collection.elements:
            clean_item(collection.type, item)
            generate_inner_struct_data(collection.type, item, request, None, True)
        if 'enforce' in request:
            for param in request:
                if param[-6:] == '-fixed':
                    target = param[:-6]
                    models.CollectionElementValue.objects.\
                        filter(element__collection=collection).\
                        filter(key__uuid=target).\
                        update(value=request[target])
    mark_task_as_done(task)


@shared_task
def duplicate_collection(task, uuid, name):
    start_task(task)
    old_collection = models.Collection.objects.get(uuid=uuid)
    collection = models.Collection.objects.create(
        name=name,
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
    mark_task_as_done(task)
