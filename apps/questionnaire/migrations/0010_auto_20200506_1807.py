# Generated by Django 3.0.3 on 2020-05-06 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_auto_20200506_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlechoosequiz',
            name='right',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questionnaire.SingleChooseVariant'),
        ),
    ]