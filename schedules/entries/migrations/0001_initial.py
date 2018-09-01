# Generated by Django 2.1.1 on 2018-09-01 08:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_effective', models.DateField(default=django.utils.timezone.now, verbose_name='Дата начала действия')),
                ('published', models.BooleanField(verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Расписнаие',
                'verbose_name_plural': 'Расписания',
            },
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, unique=True, verbose_name='Заголовок')),
                ('html', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='ScheduleEntrySection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, unique=True, verbose_name='Заголовок')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.Schedule', verbose_name='Расписание')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.AddField(
            model_name='scheduleentry',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.ScheduleEntrySection', verbose_name='Раздел'),
        ),
    ]
