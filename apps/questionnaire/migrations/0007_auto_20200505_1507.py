# Generated by Django 3.0.3 on 2020-05-05 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_auto_20200505_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arbitraryquiz',
            old_name='right',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='multichooseequiz',
            old_name='right',
            new_name='order',
        ),
        migrations.AddField(
            model_name='singlechoosequiz',
            name='order',
            field=models.SmallIntegerField(default=0),
        ),
    ]
