# Generated by Django 4.0.6 on 2022-07-15 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedChallenges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('photo_id', models.CharField(blank=True, max_length=256)),
                ('duration', models.IntegerField(default=30)),
                ('date_start', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Challenges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('photo_id', models.CharField(blank=True, max_length=256)),
                ('duration', models.IntegerField(default=30)),
                ('for_all', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('telegram_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('language_code', models.CharField(blank=True, max_length=4)),
                ('is_blocked_bot', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('time_zone', models.SmallIntegerField(default=-3)),
                ('challenge_accepted', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.acceptedchallenges')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('measurement', models.CharField(choices=[('numbers', 'Шт'), ('distance', 'Км'), ('minutes', 'Мин')], default='number', max_length=30)),
                ('amount', models.IntegerField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.challenges')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExercisesAll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('measurement', models.CharField(choices=[('numbers', 'Шт'), ('distance', 'Км'), ('minutes', 'Мин')], default='number', max_length=30)),
                ('for_all', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='challenges',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user'),
        ),
        migrations.CreateModel(
            name='AcceptedExerciseSet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('measurement', models.CharField(choices=[('numbers', 'Шт'), ('distance', 'Км'), ('minutes', 'Мин')], default='number', max_length=30)),
                ('amount', models.IntegerField()),
                ('progress', models.FloatField(default=0)),
                ('progress_on_last_day', models.FloatField(default=0)),
                ('last_day', models.DateField(blank=True, null=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.acceptedchallenges')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
