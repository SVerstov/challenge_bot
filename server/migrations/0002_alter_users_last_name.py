# Generated by Django 4.0.6 on 2022-07-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]