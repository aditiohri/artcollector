# Generated by Django 2.2 on 2020-01-01 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.CharField(max_length=300),
        ),
    ]
