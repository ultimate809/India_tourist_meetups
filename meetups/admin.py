from django.contrib import admin
from .models import Meetup, Location, Organiser, Attendees


# Register your models here.

class MeetupAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'location')
  list_filter = ('location',)
  prepopulated_fields = {"slug": ("title",)}


admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Location)
admin.site.register(Organiser)
admin.site.register(Attendees)

