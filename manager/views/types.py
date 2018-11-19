from django.shortcuts import render, redirect, get_object_or_404
from manager import models


def types(request):
    return render(request, 'types/index.html', {
        "type": None,
        "types": models.DataType.objects.all()
    })


def types_add(request):
    obj = models.DataType.objects.create(
        name=request.POST['name']
    )
    return redirect('types_detail', uuid=obj.uuid)


def types_detail(request, uuid):
    return render(
        request, 'types/edit.html', {
            'element': None,
            "type": get_object_or_404(models.DataType, uuid=uuid),
            "types": models.DataType.objects.all()
        }
    )


def types_edit(request, uuid):
    obj = get_object_or_404(models.DataType, uuid=uuid)
    obj.name = request.POST['name']
    obj.data_type = request.POST['data_type']
    if 'min' in request.POST:
        obj.min = int(request.POST['min'])
    if 'max' in request.POST:
        obj.max = int(request.POST['max'])
    if 'variants' in request.POST:
        obj.variants = request.POST['variants']
    obj.fixed = True if 'fixed' in request.POST else False

    if obj.min > obj.max:
        obj.min ^= obj.max
        obj.max ^= obj.min
        obj.min ^= obj.max

    obj.save()
    return redirect('types_detail', uuid=uuid)


def types_delete(request, uuid):
    obj = get_object_or_404(models.DataType, uuid=uuid)
    obj.delete()
    return redirect('types')


def option_add(request, uuid):
    obj = get_object_or_404(models.DataType, uuid=uuid)
    models.DataTypeOption.objects.create(
        base_type=obj,
        name=request.POST['value']
    )
    return redirect('types_detail', uuid=uuid)


def option_remove(request, uuid):
    obj = get_object_or_404(models.DataTypeOption, uuid=uuid)
    origin = obj.base_type.uuid
    obj.delete()
    return redirect('types_detail', uuid=origin)


def subtype_add(request):
    target = get_object_or_404(models.DataType, uuid=request.POST['parent'])
    target_type = get_object_or_404(models.DataType, uuid=request.POST['type'])
    obj = models.DataTypeElement.objects.create(
        name=request.POST['name'],
        base_type=target,
        data_type=target_type
    )
    return redirect('subtype_detail', uuid=obj.uuid)


def subtype_detail(request, uuid):
    element = get_object_or_404(models.DataTypeElement, uuid=uuid)
    return render(
        request, 'types/subtype.html', {
            'element': element,
            "type": element.base_type,
            "types": models.DataType.objects.all()
        }
    )


def subtype_edit(request, uuid):
    element = get_object_or_404(models.DataTypeElement, uuid=uuid)
    target_type = get_object_or_404(models.DataType, uuid=request.POST['type'])
    element.name = request.POST['name']
    element.data_type = target_type
    if 'recap' in request.POST:
        element.recap = True if 'recap' in request.POST else False
    if 'min' in request.POST:
        element.min_count = int(request.POST['min'])
    if 'max' in request.POST:
        element.max_count = int(request.POST['max'])

    if element.min_count > element.max_count:
        element.min_count ^= element.max_count
        element.max_count ^= element.min_count
        element.min_count ^= element.max_count

    element.save()
    return redirect('subtype_detail', uuid=element.uuid)


def subtypes_delete(request, uuid):
    obj = get_object_or_404(models.DataTypeElement, uuid=uuid)
    target = obj.base_type.uuid
    obj.delete()
    return redirect('types_detail', uuid=target)


def types_duplicate(request, uuid):
    old_type = get_object_or_404(models.DataType, uuid=uuid)
    new_type = models.DataType.objects.create(
        name=request.POST['name'],
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
    return redirect('types_detail', uuid=new_type.uuid)
