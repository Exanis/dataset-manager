from uuid import uuid4
from django.db import models


class DataType(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    min = models.IntegerField(default=10)
    max = models.IntegerField(default=255)
    data_type = models.CharField(max_length=10, choices=[
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
        ('lorem', 'Lorem Ipsum'),
        ('str', 'String'),
        ('options', 'Options'),
        ('struct', 'Collection'),
        ('uuid', 'UUID'),
        ('person', 'Person'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('time', 'Time')
    ], default='str')
    fixed = models.BooleanField(default=False)
    
    @property
    def options(self):
        return self.options_list.all()
    
    @property
    def fields(self):
        return self.fields_list.all()

    def __str__(self):
        return self.name
    
    class Meta():
        ordering = ['name']


class DataTypeElement(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    base_type = models.ForeignKey(DataType, related_name='fields_list', on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataType, null=True, on_delete=models.CASCADE)
    recap = models.BooleanField(default=False)
    min_count = models.PositiveSmallIntegerField(default=1)
    max_count = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['name']
        
        
class DataTypeOption(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    base_type = models.ForeignKey(DataType, related_name='options_list', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    class Meta():
        ordering = ['name']
