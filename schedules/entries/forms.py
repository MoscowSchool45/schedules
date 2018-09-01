from django import forms

from entries.models import Schedule


class ScheduleAddForm(forms.ModelForm):
    chronobus_file = forms.FileField(label="HTML расписнаие из Хронобуса", required=False)
    delete_existing = forms.BooleanField(label="Удалить имеющиеся записи", initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Do not show `delete_existing` if there is nothing to delete yet
        if not self.instance or not self.instance.pk or not self.instance.scheduleentrysection_set.exists():
            self.fields['delete_existing'].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit)
        instance.save()
        instance.load_from_file(self.cleaned_data['chronobus_file'], cleanup=self.cleaned_data['delete_existing'])
        return instance

    class Meta:
        model = Schedule
        fields = ['date_effective', 'published']
