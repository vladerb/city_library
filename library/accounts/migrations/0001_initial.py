# Generated by Django 5.1 on 2024-09-21 18:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archive', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField()),
                ('date_due', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.book')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, default='users/default_autor.webp', null=True, upload_to='users/%Y/%m/%d/')),
                ('place_of_study', models.CharField(blank=True, max_length=255)),
                ('form_of_study', models.CharField(choices=[('FT', 'Full-time'), ('PT', 'Part-time'), ('DU', 'Dual')], max_length=2)),
                ('books_received', models.ManyToManyField(blank=True, through='accounts.BookReceipt', to='archive.book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookreceipt',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
        migrations.AlterUniqueTogether(
            name='bookreceipt',
            unique_together={('profile', 'book')},
        ),
    ]
