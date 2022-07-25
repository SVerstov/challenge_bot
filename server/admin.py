from django.contrib import admin
from server.models import User, ExercisesAll, Challenges, ExerciseSet, AcceptedChallenges, AcceptedExerciseSet


@admin.action(description='Mark selected available for all users')
def make_for_all(modeladmin, request, queryset):
    queryset.update(for_all=True)

class UsersAdmin(admin.ModelAdmin):
    pass


class ExercisesAllAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement','for_all']
    actions = [make_for_all]


class ChallengesAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'for_all']
    actions = [make_for_all]


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
