# Generated by Django 5.1.2 on 2024-10-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_slug_to_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(default='', max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('F', 'Failed'), ('P', 'Pending'), ('C', 'Complete')], default='P', max_length=1),
        ),
    ]
