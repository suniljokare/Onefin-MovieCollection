# Generated by Django 4.2.5 on 2023-09-23 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_movie_uuid_alter_collection_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together=set(),
        ),
    ]