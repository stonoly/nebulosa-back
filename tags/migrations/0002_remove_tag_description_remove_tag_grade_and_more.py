# Generated by Django 5.1.5 on 2025-05-15 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_placeadress_remove_place_latitude_and_more'),
        ('tags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='places',
        ),
        migrations.CreateModel(
            name='PlaceTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('grade', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_tags', to='places.place')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_tags', to='tags.tag')),
            ],
            options={
                'unique_together': {('tag', 'place')},
            },
        ),
    ]
