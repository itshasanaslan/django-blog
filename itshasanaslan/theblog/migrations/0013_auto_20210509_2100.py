# Generated by Django 3.1.6 on 2021-05-09 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0012_post_is_visible_on_main_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_visible_on_main_page',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
