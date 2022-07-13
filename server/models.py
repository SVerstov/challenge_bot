from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Users(models.Model):
    telegram_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)

    challenge_accepted = models.ForeignKey('Challenges', on_delete=models.DO_NOTHING, blank=True, null=True,
                                           default=None)
    date_start = models.DateField(blank=True, null=True, default=None)

    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", blank=True)
    is_blocked_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    time_zone = models.SmallIntegerField(default=-3)

    def __str__(self):
        return self.username if self.username else str(self.telegram_id)


class Exercise(models.Model):
    MEASUREMENTS = [
        ('numbers', 'количество'),
        ('distance', 'расстояние, Км'),
        ('minutes', 'минуты'),
    ]

    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey('Users', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=30)
    for_all = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    measurement = models.CharField(default='number', max_length=30, choices=MEASUREMENTS)

    def __str__(self):
        return self.name


class Challenges(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey('Users', on_delete=models.DO_NOTHING, blank=True, null=True)
    main_copy = models.BooleanField(default=False)
    for_all = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    photo_id = models.CharField(max_length=256, blank=True)
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class CurrentChallenge(models.Model):
    id = models.AutoField(primary_key=True)
    challenge = models.ForeignKey('Challenges', on_delete=models.DO_NOTHING, null=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.DO_NOTHING, null=True)
    exercises_amount = models.PositiveIntegerField()
    exercises_done = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.challenge_id)
