# Generated by Django 4.2.5 on 2023-10-15 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_img', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carosel1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel1', models.TextField()),
                ('status', models.TextField(default='Carosel1')),
            ],
        ),
        migrations.CreateModel(
            name='Carosel2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel2', models.TextField()),
                ('status', models.TextField(default='Carosel2')),
            ],
        ),
        migrations.CreateModel(
            name='Carosel3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel3', models.TextField()),
                ('status', models.TextField(default='Carosel3')),
            ],
        ),
        migrations.DeleteModel(
            name='Admin_img',
        ),
    ]