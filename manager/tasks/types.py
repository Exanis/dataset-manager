from celery import shared_task
from manager import models


@shared_task
def duplicate_type(uuid, name):
    old_type = models.DataType.objects.get(uuid=uuid)
    new_type = models.DataType.objects.create(
        name=name,
        min=old_type.min,
        max=old_type.max,
        data_type=old_type.data_type,
        fixed=old_type.fixed
    )
    for option in old_type.options:
        models.DataTypeOption.objects.create(
            base_type=new_type,
            name=option.name
        )
    for field in old_type.fields:
        models.DataTypeElement.objects.create(
            name=field.name,
            base_type=new_type,
            data_type=field.data_type,
            recap=field.recap,
            min_count=field.min_count,
            max_count=field.max_count
        )