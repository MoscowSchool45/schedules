from django.urls import path

from entries.views import EntryDetailView, IndexView, ScheduleDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='entry-index'),
    path('<slug:sched_slug>-<sched_pk>/', ScheduleDetailView.as_view(), name='entry-schedule-detail'),
    path('<slug:sched_slug>-<sched_pk>/<slug:slug>-<pk>/', EntryDetailView.as_view(), name='entry-entry-detail'),
]
