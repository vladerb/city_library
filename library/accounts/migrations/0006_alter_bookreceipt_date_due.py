# Generated by Django 5.1 on 2024-09-24 15:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_bookreceipt_date_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreceipt',
            name='date_due',
            field=models.DateField(default=datetime.datetime(2024, 10, 1, 18, 57, 46, 484152)),
        ),
    ]
