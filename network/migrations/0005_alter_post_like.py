# Generated by Django 4.2.4 on 2023-09-29 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_like_id_alter_post_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]