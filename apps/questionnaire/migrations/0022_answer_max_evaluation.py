# Generated by Django 3.0.6 on 2020-05-17 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0021_auto_20200516_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='max_evaluation',
            field=models.SmallIntegerField(null=True),
        ),
    ]
