# Generated by Django 2.2.3 on 2019-07-20 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0010_auto_20190720_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='title_ru',
            new_name='title',
        ),
    ]
