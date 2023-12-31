# Generated by Django 4.2.5 on 2023-09-30 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFile',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoTranscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcription', models.TextField()),
                ('description', models.TextField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='video.videofile')),
            ],
        ),
        migrations.CreateModel(
            name='VideoChunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chunk_number', models.PositiveIntegerField()),
                ('chunk_path', models.CharField(max_length=255)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.videofile')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteVideoURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('embedded_url', models.URLField(max_length=255)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.videofile')),
            ],
        ),
    ]
