# Generated by Django 4.2.4 on 2023-09-29 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_remove_user_followers_remove_user_following_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liker',
        ),
    ]