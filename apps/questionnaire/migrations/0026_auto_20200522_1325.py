# Generated by Django 3.0.6 on 2020-05-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0025_auto_20200520_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multichoosequiz',
            name='method',
        ),
        migrations.RemoveField(
            model_name='multichoosequiz',
            name='scale_value',
        ),
        migrations.AlterField(
            model_name='answer',
            name='evaluation',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
