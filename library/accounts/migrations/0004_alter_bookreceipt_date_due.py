# Generated by Django 5.1 on 2024-09-23 23:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_bookreceipt_date_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreceipt',
            name='date_due',
            field=models.DateField(default=datetime.datetime(2024, 10, 1, 2, 55, 8, 840389)),
        ),
    ]
