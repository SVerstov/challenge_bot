from django.db import models


class User(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", blank=True)
    is_blocked_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    time_zone = models.SmallIntegerField(default=-3)

    def __str__(self):
        return self.username


class Exercise(models.Model):
    MEASUREMENTS = [
        ('numbers', 'количество'),
        ('distance', 'расстояние'),
    ]

    id = models.IntegerField(primary_key=True)
    user_created = models.ForeignKey('User')  # ???
    name = models.CharField()
    description = models.TextField(blank=True)
    measurement = models.CharField(default='number', choices=MEASUREMENTS)


class Challenges(models.Model):
    id = models.IntegerField(primary_key=True)
    user_created = models.ForeignKey('User')  # ???
    name = models.CharField()
    description = models.TextField(blank=True)
    photo = models.TextField(blank=True)
    duration = models.IntegerField(default=30)
    # exercise_set =