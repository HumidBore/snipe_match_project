# Generated by Django 3.1.7 on 2021-03-14 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='discussione_appartenenza',
            new_name='discussione',
        ),
    ]
