# Generated by Django 3.0.6 on 2020-05-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_auto_20200503_1328'),
        ('questionnaire', '0015_auto_20200510_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='questionnaires', to='administration.Departament'),
        ),
    ]