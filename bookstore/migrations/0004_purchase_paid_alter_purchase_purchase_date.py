# Generated by Django 4.1.5 on 2023-03-10 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_bookcategory_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
