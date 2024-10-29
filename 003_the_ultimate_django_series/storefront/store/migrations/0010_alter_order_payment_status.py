# Generated by Django 5.1.2 on 2024-10-29 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_cartitem_quantity_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('C', 'Complete'), ('F', 'Failed'), ('P', 'Pending')], default='P', max_length=1),
        ),
    ]
