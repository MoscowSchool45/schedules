from functools import update_wrapper

import nested_admin
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from entries.models import Schedule, ScheduleEntry, ScheduleEntrySection
from entries.views import ChronobusUploadView


class ScheduleEntryInline(nested_admin.NestedTabularInline):
    model = ScheduleEntry
    fields = ('title', )


class ScheduleEntrySectionInline(nested_admin.NestedTabularInline):
    model = ScheduleEntrySection
    inlines = (ScheduleEntryInline,)


class ScheduleAdmin(nested_admin.NestedModelAdmin):
    inlines = (ScheduleEntrySectionInline, )
    save_on_top = True

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            path(
                'chronobus_upload/',
                wrap(ChronobusUploadView.as_view()),
                name='%s_%s_chronobus_upload' % info
            ),
            path(
                '<pk>/chronobus_upload/',
                wrap(ChronobusUploadView.as_view()),
                name='%s_%s_chronobus_upload_add' % info
            ),
        ]
        return my_urls + urls

    def add_files_url(self):
        url = reverse('admin:entries_schedule_chronobus_upload_add', kwargs={'pk': self.pk})
        return format_html('<a href="{}">Добавить данные из файла</a>', url)

    add_files_url.short_description = 'Хронобус'
    list_display = ('__str__', 'entry_count', add_files_url)

class ScheduleEntrySectionAdmin(admin.ModelAdmin):
    inlines = (ScheduleEntryInline, )


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleEntry, admin.ModelAdmin)
admin.site.register(ScheduleEntrySection, ScheduleEntrySectionAdmin)
