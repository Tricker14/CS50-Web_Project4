# Generated by Django 4.2.4 on 2023-10-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]