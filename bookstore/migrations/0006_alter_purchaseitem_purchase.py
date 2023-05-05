# Generated by Django 4.1.5 on 2023-03-17 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_alter_purchase_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='bookstore.purchase'),
        ),
    ]
