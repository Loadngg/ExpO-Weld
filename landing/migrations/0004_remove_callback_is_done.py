# Generated by Django 3.2.25 on 2024-08-02 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_callback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callback',
            name='is_done',
        ),
    ]