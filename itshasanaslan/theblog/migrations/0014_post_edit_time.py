# Generated by Django 3.1.6 on 2021-05-30 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0013_auto_20210509_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edit_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
