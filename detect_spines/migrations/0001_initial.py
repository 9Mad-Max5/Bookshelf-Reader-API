# Generated by Django 4.1.7 on 2023-03-14 14:15

import detect_spines.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('rating', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('publisher', models.CharField(blank=True, max_length=500, null=True)),
                ('isbn_10', models.CharField(blank=True, max_length=20, null=True)),
                ('isbn_13', models.CharField(blank=True, max_length=20, null=True)),
                ('total_pages', models.CharField(blank=True, max_length=10, null=True)),
                ('genre', models.CharField(blank=True, max_length=500, null=True)),
                ('dimensions', models.CharField(blank=True, max_length=500, null=True)),
                ('book_cover_url', models.CharField(blank=True, max_length=32656232365, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bookshelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=detect_spines.models.bookshelf_image_path)),
                ('spine_line_drawn_image', models.ImageField(blank=True, null=True, upload_to=detect_spines.models.spine_drawn_bookshelf_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='Spine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=detect_spines.models.spine_image_path)),
                ('bookshelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect_spines.bookshelf')),
            ],
        ),
    ]
