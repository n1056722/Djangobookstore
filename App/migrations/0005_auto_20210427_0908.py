# Generated by Django 2.2.9 on 2021-04-27 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20210426_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Author'),
        ),
    ]
