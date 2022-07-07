from django.contrib import admin
from server.models import Users, Exercise, CurrentChallenge, Challenges


class UsersAdmin(admin.ModelAdmin):
    pass


class ExerciseAdmin(admin.ModelAdmin):
    pass


class ChallengesAdmin(admin.ModelAdmin):
    pass


class CurrentChallengeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Users, UsersAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(CurrentChallenge, CurrentChallengeAdmin)
admin.site.register(Challenges, ChallengesAdmin)
