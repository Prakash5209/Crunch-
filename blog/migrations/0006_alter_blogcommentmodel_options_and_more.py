# Generated by Django 5.0.1 on 2024-02-03 13:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogcommentmodel_parent_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcommentmodel',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='createblogmodel',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='blogcommentmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogcommentmodel',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]