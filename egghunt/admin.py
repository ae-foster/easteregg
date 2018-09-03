from django.contrib import admin

from .models import Egg, LeaderboardEntry, Image, Downtime


admin.site.register(LeaderboardEntry)
admin.site.register(Downtime)


# This allows us to change the images within the egg admin page
class InlineImage(admin.TabularInline):
    model = Image
    extra = 1


class EggAdmin(admin.ModelAdmin):
    inlines = [InlineImage]


admin.site.register(Egg, EggAdmin)
