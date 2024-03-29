# Generated by Django 4.2.4 on 2023-10-01 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_rename_user_follow_username_alter_follow_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='username',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='user_being_followed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
