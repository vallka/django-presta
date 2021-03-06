# Generated by Django 3.1 on 2020-08-27 23:50

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('keywords', models.TextField(blank=True, default='', verbose_name='Meta Keywords')),
                ('json_ld', models.TextField(blank=True, default='', verbose_name='script ld+json')),
                ('text', markdownx.models.MarkdownxField(blank=True, verbose_name='Text')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
    ]
