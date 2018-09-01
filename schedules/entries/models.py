from bs4 import BeautifulSoup
from django.db import models
from django.utils import timezone, text

from unidecode import unidecode


class Schedule(models.Model):
    date_effective = models.DateField(default=timezone.now, verbose_name="Дата начала действия")
    published = models.BooleanField(verbose_name="Опубликовано")

    @property
    def slug(self):
        return text.slugify(self.date_effective.strftime("%d%m%y"))

    def __str__(self):
        return "Расписание от " + self.date_effective.strftime("%d/%m/%y")

    @classmethod
    def active(cls):
        return cls.archive().first()

    @classmethod
    def archive(cls):
        return cls.objects.filter(published=True)

    def entry_count(self):
        return ScheduleEntry.objects.filter(section__in = self.scheduleentrysection_set.all()).count()
    entry_count.short_description = "Количество записей"

    def load_from_file(self, file, cleanup=False):
        parser = BeautifulSoup(file, 'html.parser')
        if cleanup:
            self.scheduleentrysection_set.all().delete()

        if not parser.body:
            return False
        section_title = parser.title.get_text() or parser.body.title.get_text() or "Иное"
        entries = parser.body.find_all('table', recursive=False)
        section, _ = self.scheduleentrysection_set.get_or_create(title=section_title)
        for entry_table in entries:
            entry_title = entry_table.caption.get_text() or "Иное"
            entry, _ = section.scheduleentry_set.get_or_create(title=entry_title)
            entry.html = entry_table.prettify()
            entry.save()
        return True

    class Meta:
        verbose_name = "Расписнаие"
        verbose_name_plural = "Расписания"
        ordering = ("-date_effective", )


class ScheduleEntrySection(models.Model):
    title = models.CharField(max_length=1024, verbose_name="Заголовок")
    schedule = models.ForeignKey(Schedule, verbose_name="Расписание", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.schedule} - {self.title} ({self.scheduleentry_set.count()})"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        unique_together = ('title', 'schedule')
        ordering = ("title", )


class ScheduleEntry(models.Model):
    title = models.CharField(max_length=1024, verbose_name="Заголовок")
    html = models.TextField(blank=True)
    section = models.ForeignKey(ScheduleEntrySection, verbose_name="Раздел", on_delete=models.CASCADE)\

    @property
    def slug(self):
        return text.slugify(unidecode(self.title))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        unique_together = ('title', 'section')
        ordering = ("title", )
