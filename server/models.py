from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

bn = dict(blank=True, null=True)


class User(models.Model):
    telegram_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, **bn)
    first_name = models.CharField(max_length=256, **bn)
    last_name = models.CharField(max_length=256, **bn)
    language_code = models.CharField(max_length=4, blank=True)
    challenge_accepted = models.OneToOneField('AcceptedChallenges', **bn, on_delete=models.SET_NULL, default=None)
    is_blocked_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    time_zone = models.SmallIntegerField(default=3)

    def __str__(self):
        return self.username if self.username else str(self.telegram_id)


class BaseExercise(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']

    MEASUREMENTS = [
        ('numbers', 'Шт'),
        ('distance', 'Км'),
        ('minutes', 'Мин'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    measurement = models.CharField(default='number', max_length=30, choices=MEASUREMENTS)

    def __str__(self):
        return self.name


class ExercisesAll(BaseExercise):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    for_all = models.BooleanField(default=False)


class ExerciseSet(BaseExercise):
    challenge = models.ForeignKey('Challenges', on_delete=models.CASCADE)
    amount = models.IntegerField()


class AcceptedExerciseSet(BaseExercise):
    challenge = models.ForeignKey('AcceptedChallenges', on_delete=models.CASCADE)
    amount = models.IntegerField()
    progress = models.FloatField(default=0)
    progress_on_last_day = models.FloatField(default=0)
    last_day = models.DateField(**bn)


class BaseChallenges(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    photo_id = models.CharField(max_length=256, blank=True)
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class Challenges(BaseChallenges):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)

    for_all = models.BooleanField(default=False)


class AcceptedChallenges(BaseChallenges):
    date_start = models.DateField()


