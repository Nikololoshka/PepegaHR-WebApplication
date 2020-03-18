# Generated by Django 3.0.3 on 2020-03-18 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_auto_20200313_0716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hruser',
            options={'managed': True, 'verbose_name': 'HRUser', 'verbose_name_plural': 'HRUsers'},
        ),
        migrations.RemoveField(
            model_name='hruser',
            name='profile',
        ),
        migrations.AddField(
            model_name='hruser',
            name='photo',
            field=models.ImageField(default='user-photos/default.png', upload_to='user-photos/'),
        ),
        migrations.AddField(
            model_name='hruser',
            name='role',
            field=models.CharField(choices=[('adm', 'Администратор'), ('mod', 'Модератор'), ('usr', 'Пользователь')], default='usr', max_length=3),
        ),
        migrations.AlterField(
            model_name='departament',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.Departament'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
