# Generated by Django 3.2 on 2021-04-12 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blind',
            name='photo',
            field=models.ImageField(upload_to='products'),
        ),
    ]
