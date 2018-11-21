from random import randint
from celery import shared_task
from manager import models, validators, generators
from .utils import mark_task_as_done, start_task


def generate(item, field, count, cnt=None):
    gen = getattr(generators, field.data_type.data_type + "_generator")
    if cnt is None:
        cnt = len(item.values_for(field))
    for _ in range(count):
        value = gen(field.data_type, cnt)
        cnt += 1
        models.CollectionElementValue.objects.create(
            element=item,
            key=field,
            value=value
        )


def make_visible_list(target_type, include_all=False, prefix='', forbidden=None):
    result = []
    if forbidden is None:
        forbidden = []
    if target_type in forbidden:
        return result
    for field in target_type.fields:
        if field.recap or include_all:
            if field.data_type.data_type == 'struct':
                result = result + make_visible_list(
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


@shared_task
def generate_collection(task, uuid, request):
    start_task(task)
    collection = models.Collection.objects.get(uuid=uuid)
    generate_count = int(request['count'])
    fields = make_visible_list(collection.type, include_all=True)
    for _ in range(generate_count):
        item = models.CollectionElement.objects.create(collection=collection)
        for field_base in fields:
            field = field_base['field']
            count = randint(field.min_count, field.max_count)
            if str(field.uuid) + '-fixed' in request:
                val = request[str(field.uuid)]
                if field.data_type.data_type in ['datetime', 'time']:
                    timeval = val.split('T')
                    timepart = timeval[1] if len(timeval) == 2 else timeval[0]
                    datepart = timeval[0] + 'T' if len(timeval) == 2 else ''
                    if len(timepart) == 5:
                        timepart += ':00'
                    val = datepart + timepart
                for __ in range(count):
                    models.CollectionElementValue.objects.create(
                        element=item,
                        key=field,
                        value=val
                    )
            else:
                generate(item, field, count)
    mark_task_as_done(task)


@shared_task
def fix_collection(task, uuid, request):
    start_task(task)
    collection = models.Collection.objects.get(uuid=uuid)
    fields = make_visible_list(collection.type, include_all=True)
    enforce = 'enforce' in request
    generate_all = 'all' in request
    for item in collection.elements:
        for field_base in fields:
            field = field_base['field']
            if str(field.uuid) + '-fixed' in request and enforce:
                item.values_for(field).delete()
                count = randint(field.min_count, field.max_count)
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
                        value=val
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
                    if str(field.uuid) + '-fixed' in request:
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
                                value=val
                            )
                    else:
                        generate(item, field, count, existing)
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
