# Generated by Django 3.2.25 on 2024-07-29 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_productdocument_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspectype',
            name='is_filter',
            field=models.BooleanField(default=False, verbose_name='Является фильтром'),
        ),
    ]
