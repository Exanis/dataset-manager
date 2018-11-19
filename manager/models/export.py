from uuid import uuid4
from django.db import models


class Export(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=[
        ('json', 'Json'),
        ('api', 'API'),
        ('db', 'Database')
    ], default='json')
    username = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, default='')
    method = models.CharField(max_length=6, default='POST')
    flatten = models.BooleanField(default=False)

    @property
    def params(self):
        return self.params_list.all()

    class Meta():
        ordering = ['name']


class ExportParam(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    export = models.ForeignKey(Export, on_delete=models.CASCADE, related_name='params_list')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=2048)
