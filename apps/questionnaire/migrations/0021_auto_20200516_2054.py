# Generated by Django 3.0.6 on 2020-05-16 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0020_auto_20200515_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='is_complite',
            new_name='is_complete',
        ),
        migrations.AddField(
            model_name='answer',
            name='evaluation',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questionnaire.Questionnaire'),
        ),
    ]