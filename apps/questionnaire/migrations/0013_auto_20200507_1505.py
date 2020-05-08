# Generated by Django 3.0.3 on 2020-05-07 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0012_multichooseevariant_right'),
    ]
    atomic = False

    operations = [
        migrations.RenameModel(
            old_name='MultiChooseeQuiz',
            new_name='MultiChooseQuiz',
        ),
        migrations.RenameModel(
            old_name='MultiChooseeVariant',
            new_name='MultiChooseVariant',
        ),
        migrations.AlterModelOptions(
            name='multichoosequiz',
            options={'managed': True, 'verbose_name': 'MultiChooseQuiz', 'verbose_name_plural': 'MultiChooseQuizzes'},
        ),
        migrations.AlterModelOptions(
            name='multichoosevariant',
            options={'managed': True, 'ordering': ['order', 'variant'], 'verbose_name': 'MultiChooseVariant', 'verbose_name_plural': 'MultiChooseVariants'},
        ),
    ]