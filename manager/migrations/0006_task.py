# Generated by Django 2.1.3 on 2018-11-20 23:51

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20181120_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('start', models.DateTimeField(default=None, null=True)),
                ('end', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'ordering': ['-end', '-start', 'registered'],
            },
        ),
    ]