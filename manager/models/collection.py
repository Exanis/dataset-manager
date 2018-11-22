from uuid import uuid4
from django.db import models
from manager import validators


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.ForeignKey('manager.DataType', related_name='collections', on_delete=models.CASCADE)

    @property
    def elements(self):
        return self.elements_list.all()

    class Meta():
        ordering = ['name']


def _check_item_valid(t, item, parent):
    for field in t.fields:
        if not item.is_field_valid(field, parent):
            return False
    return True


class CollectionElement(models.Model):
    def __init__(self, *args, **kwargs):
        self._values_for_cached = {}
        super(CollectionElement, self).__init__(*args, **kwargs)

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.PositiveSmallIntegerField(default=0)
    collection = models.ForeignKey(Collection, related_name='elements_list', on_delete=models.CASCADE)

    @property
    def is_valid(self):
        return _check_item_valid(self.collection.type, self, None)

    @property
    def values(self):
        return self.values_list.all()

    def values_for(self, target_type):
        if target_type not in self._values_for_cached:
            self._values_for_cached[target_type] = self.values_list.filter(key=target_type)
        return self._values_for_cached[target_type]

    def is_field_valid(self, field, parent=None):
        values = self.values_for(field).filter(parent=parent)
        cnt = len(values)
        if cnt < field.min_count or cnt > field.max_count:
            return False
        if field.data_type.data_type == 'struct':
            for val in values:
                if not _check_item_valid(field.data_type, self, val):
                    return False
        else:
            validator = getattr(validators, field.data_type.data_type + '_validator')
            for val in values:
                if not validator(val.value, field.data_type):
                    return False
        return True

    class Meta():
        ordering = ['order']


class CollectionElementValue(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    element = models.ForeignKey(CollectionElement, related_name='values_list', on_delete=models.CASCADE)
    value = models.CharField(max_length=2048)
    key = models.ForeignKey('manager.DataTypeElement', on_delete=models.CASCADE)
    parent = models.ForeignKey('manager.CollectionElementValue', null=True, default=None, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta():
        ordering = ['order']
