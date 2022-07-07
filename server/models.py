from django.db import models


class Users(models.Model):
    telegram_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
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
    created_by = models.ForeignKey('Users', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    measurement = models.CharField(default='number', max_length=30, choices=MEASUREMENTS)

    def __str__(self):
        return self.name


class Challenges(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    photo_id = models.TextField(blank=True)  # id телеграм файла
    duration = models.IntegerField(default=30)
    created_by = models.ForeignKey('Users', on_delete=models.CASCADE)
    exercise_set = models.TextField()

    def __str__(self):
        return self.name


class CurrentChallenge():
    launched_by = models.ForeignKey('User', on_delete=models.CASCADE, primary_key=True)
    challenge = models.ForeignKey('Challenges', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    date_start = models.DateField(auto_now_add=True)
    progress = models.TextField()

    def __str__(self):
        return self.name
