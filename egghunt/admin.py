from django.contrib import admin

# Register your models here.
from .models import Egg, LeaderboardEntry, Image, Downtime


admin.site.register(LeaderboardEntry)

class InlineImage(admin.TabularInline):
    model = Image
    extra = 1

class EggAdmin(admin.ModelAdmin):
    inlines = [InlineImage]


admin.site.register(Egg, EggAdmin)

admin.site.register(Downtime)
