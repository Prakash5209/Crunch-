# Generated by Django 5.0.1 on 2024-02-12 11:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_rename_follower_follow_follow_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='follow',
            name='youser',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='follow',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='follow',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='follow_back',
        ),
    ]