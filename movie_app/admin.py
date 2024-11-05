from django.contrib import admin
from .models import Director, Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'duration')

admin.site.register(Director)
admin.site.register(Review)

