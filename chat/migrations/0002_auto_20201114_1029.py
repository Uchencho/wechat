# Generated by Django 3.1.2 on 2020-11-14 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['-id']},
        ),
    ]
