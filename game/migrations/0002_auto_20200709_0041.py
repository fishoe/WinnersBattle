# Generated by Django 3.0.8 on 2020-07-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
