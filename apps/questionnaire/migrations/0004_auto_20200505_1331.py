# Generated by Django 3.0.3 on 2020-05-05 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20200505_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='singlechoosevariant',
            name='variant',
            field=models.TextField(blank=True, max_length=256),
        ),
    ]
