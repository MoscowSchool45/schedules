from django import forms

from entries.models import Schedule


class ScheduleAddForm(forms.ModelForm):
    chronobus_file = forms.FileField(
        label="HTML расписнаие из Хронобуса",
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    delete_existing = forms.BooleanField(label="Удалить имеющиеся записи", initial=False, required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Do not show `delete_existing` if there is nothing to delete yet
        if not self.instance or not self.instance.pk or not self.instance.scheduleentrysection_set.exists():
            self.fields['delete_existing'].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit)
        if self.request:
            files = self.request.FILES.getlist('chronobus_file')
            cleanup = self.cleaned_data['delete_existing']
            if files:
                instance.save()
                for file in files:
                    instance.load_from_file(file, cleanup=cleanup)
                    cleanup = False     # Only cleanup once
        return instance

    class Meta:
        model = Schedule
        fields = ['date_effective', 'published']
