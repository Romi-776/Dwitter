# Generated by Django 3.1.7 on 2021-05-23 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_auto_20210522_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=''),
        ),
    ]