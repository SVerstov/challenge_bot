# Generated by Django 4.0.6 on 2022-07-10 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenges',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='challenges',
            name='exercise_set',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='created_by',
        ),
        migrations.AddField(
            model_name='challenges',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='server.users'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='server.users'),
        ),
        migrations.AddField(
            model_name='users',
            name='challenge_accepted',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='server.challenges'),
        ),
        migrations.AddField(
            model_name='users',
            name='date_start',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='challenges',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='challenges',
            name='photo_id',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='measurement',
            field=models.CharField(choices=[('numbers', 'количество'), ('distance', 'расстояние'), ('minutes', 'минуты')], default='number', max_length=30),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.CreateModel(
            name='CurrentChallenge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('exercises_amount', models.PositiveIntegerField()),
                ('exercises_done', models.PositiveIntegerField(blank=True)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='server.challenges')),
                ('exercise_id', models.ManyToManyField(to='server.exercise')),
            ],
        ),
    ]