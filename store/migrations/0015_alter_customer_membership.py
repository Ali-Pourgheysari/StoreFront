# Generated by Django 4.1.7 on 2023-03-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='membership',
            field=models.CharField(choices=[('G', 'Gold'), ('S', 'Silver'), ('B', 'Bronze')], default='B', max_length=1),
        ),
    ]
