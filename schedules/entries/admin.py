from django.contrib import admin

from entries.forms import ScheduleAddForm
from entries.models import Schedule, ScheduleEntry, ScheduleEntrySection


class ScheduleEntrySectionInline(admin.TabularInline):
    model = ScheduleEntrySection


class ScheduleEntryInline(admin.TabularInline):
    model = ScheduleEntry


class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAddForm
    inlines = (ScheduleEntrySectionInline, )


class ScheduleEntrySectionAdmin(admin.ModelAdmin):
    inlines = (ScheduleEntryInline, )


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleEntry, admin.ModelAdmin)
admin.site.register(ScheduleEntrySection, ScheduleEntrySectionAdmin)
