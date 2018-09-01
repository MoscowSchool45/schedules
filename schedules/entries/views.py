from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from entries.forms import ScheduleAddForm
from entries.models import Schedule


class ChronobusUploadView(FormView, UserPassesTestMixin):
    template_name = 'chronobus_upload.html'
    form_class = ScheduleAddForm
    success_url = reverse_lazy('admin:entries_schedule_changelist')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'pk' in self.kwargs and self.kwargs['pk'] != 'None':
            instance = get_object_or_404(Schedule, pk=self.kwargs['pk'])
            kwargs.update({'instance': instance})
        kwargs.update({'request': self.request})
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        context.update({'test': 'test',
            'opts': ScheduleAddForm.Meta.model._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'site_url': '/',
            'has_permission': True,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': True,
            'has_view_permission': True,
            'has_editable_inline_admin_formsets': False,
            'add': False,
        })
        return super().render_to_response(context, **response_kwargs)
