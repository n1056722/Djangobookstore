# Generated by Django 2.2.9 on 2021-04-26 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_auto_20210425_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='author_name',
            new_name='author',
        ),
    ]
