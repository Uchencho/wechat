# Generated by Django 3.1.2 on 2020-10-25 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
