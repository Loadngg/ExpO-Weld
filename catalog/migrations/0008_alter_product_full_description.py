# Generated by Django 3.2.25 on 2024-07-13 23:24

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20240714_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='full_description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Полное описание'),
        ),
    ]
