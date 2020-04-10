from django.contrib import admin

from .models import Egg, LeaderboardEntry, Image, Downtime, Answer


admin.site.register(LeaderboardEntry)
admin.site.register(Downtime)


# This allows us to change the images within the egg admin page
class InlineImage(admin.TabularInline):
    model = Image
    extra = 1

# This allows us to change the images within the egg admin page
class InlineAnswer(admin.TabularInline):
    model = Answer
    extra = 1


class EggAdmin(admin.ModelAdmin):
    inlines = [InlineImage, InlineAnswer]


admin.site.register(Egg, EggAdmin)
