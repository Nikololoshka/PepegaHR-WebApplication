# Generated by Django 3.0.3 on 2020-05-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_auto_20200505_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlechoosevariant',
            name='variant',
            field=models.TextField(max_length=256),
        ),
    ]
