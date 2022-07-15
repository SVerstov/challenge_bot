from django.contrib import admin
from server.models import User, ExercisesAll, Challenges, ExerciseSet, AcceptedChallenges, AcceptedExerciseSet


class UsersAdmin(admin.ModelAdmin):
    pass


class ExercisesAllAdmin(admin.ModelAdmin):
    pass


class ChallengesAdmin(admin.ModelAdmin):
    pass


class ExerciseSetAdmin(admin.ModelAdmin):
    pass

class AcceptedChallengesAdmin(admin.ModelAdmin):
    pass

class AcceptedExerciseSetAdmin(admin.ModelAdmin):
    pass



admin.site.register(User, UsersAdmin)
admin.site.register(ExercisesAll, ExercisesAllAdmin)
admin.site.register(Challenges, ChallengesAdmin)
admin.site.register(ExerciseSet, ExerciseSetAdmin)
admin.site.register(AcceptedChallenges, AcceptedChallengesAdmin)
admin.site.register(AcceptedExerciseSet, AcceptedExerciseSetAdmin)