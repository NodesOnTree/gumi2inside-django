# Generated by Django 4.2.5 on 2023-09-24 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_textcolor_article_textsize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='textcolor',
        ),
        migrations.RemoveField(
            model_name='article',
            name='textsize',
        ),
    ]
