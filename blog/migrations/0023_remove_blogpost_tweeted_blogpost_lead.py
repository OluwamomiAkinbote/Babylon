# Generated by Django 4.2.5 on 2025-05-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_category_parent_delete_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='tweeted',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='lead',
            field=models.TextField(blank=True, null=True),
        ),
    ]
