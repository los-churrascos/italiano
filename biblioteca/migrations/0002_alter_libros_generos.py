# Generated by Django 3.2.4 on 2021-10-11 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libros',
            name='generos',
            field=models.TextField(),
        ),
    ]
