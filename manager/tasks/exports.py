from celery import shared_task
from manager import models
from .utils import mark_task_as_done, start_task


@shared_task
def duplicate_export(task, uuid, name):
    start_task(task)
    old_export = models.Export.objects.get(uuid=uuid)
    export = models.Export.objects.create(
        name=name,
        type=old_export.type,
        username=old_export.username,
        password=old_export.password,
        url=old_export.url,
        method=old_export.method,
        flatten=old_export.flatten
    )
    for param in old_export.params:
        models.ExportParam.objects.create(
            export=export,
            name=param.name,
            value=param.value
        )
    mark_task_as_done(task)
