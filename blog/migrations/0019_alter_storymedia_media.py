# Generated by Django 4.2.5 on 2025-04-05 19:43

from django.db import migrations
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0017_image__transparent'),
        ('blog', '0018_remove_story_created_at_story_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storymedia',
            name='media',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='story_media', to='filer.file'),
        ),
    ]
