# Generated by Django 3.2.25 on 2024-07-13 23:20

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_productspec_productspectype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='bundling',
            field=tinymce.models.HTMLField(default='', verbose_name='Комплектация'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=tinymce.models.HTMLField(default='', verbose_name='Особенности'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='full_description',
            field=tinymce.models.HTMLField(default='', verbose_name='Полное описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(default='', verbose_name='Краткое описание'),
            preserve_default=False,
        ),
    ]
