# Generated by Django 4.2.5 on 2023-10-15 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_comment_disliked_users_comment_liked_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='disliked_users',
            new_name='comment_disliked_users',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='liked_users',
            new_name='comment_liked_users',
        ),
    ]
