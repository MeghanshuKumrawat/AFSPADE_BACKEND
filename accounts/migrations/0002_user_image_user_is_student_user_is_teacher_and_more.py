# Generated by Django 4.2.1 on 2024-08-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.FileField(default='profiles/default.png', upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.CharField(choices=[('Level 100', 'Level 100'), ('Level 200', 'Level 200'), ('Level 300', 'Level 300'), ('Level 400', 'Level 400')], default='Level 100', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='matriculation_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='semester',
            field=models.CharField(choices=[('Semester 1', 'Semester 1'), ('Semester 2', 'Semester 2')], default='Semester 1', max_length=50),
        ),
    ]
