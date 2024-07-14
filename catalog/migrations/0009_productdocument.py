# Generated by Django 3.2.25 on 2024-07-14 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_product_full_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('file', models.FileField(upload_to='product/docs', verbose_name='Документ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Документ товара',
                'verbose_name_plural': 'Документы товара',
            },
        ),
    ]