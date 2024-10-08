# Generated by Django 5.1.1 on 2024-10-04 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_course_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='question',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='is_final',
        ),
        migrations.AddField(
            model_name='assignment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='assignments/'),
        ),
        migrations.AddField(
            model_name='submission',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submissions', to='main.assignment'),
        ),
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='submissions/'),
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
