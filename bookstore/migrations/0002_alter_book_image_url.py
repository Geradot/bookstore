# Generated by Django 4.1.5 on 2023-03-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
