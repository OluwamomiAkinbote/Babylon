# Generated by Django 5.0.6 on 2024-09-16 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_trend_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trend',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]