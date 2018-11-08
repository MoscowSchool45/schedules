from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from entries.models import Schedule


class ScheduleImportTestCase(TestCase):
    def test_upload_fails_without_access(self):
        """Test if schedule upload form redirects to login if not authenticated"""
        client = Client()
        response = client.get(reverse('admin:entries_schedule_chronobus_upload'))
        self.assertEqual(response.status_code, 302)

    def test_single_file_upload(self):
        """Test if it is possible to upload a schedule"""
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        client = Client()
        client.login(username = 'admin', password='password')

        # Upload view is rendered
        response = client.get(reverse('admin:entries_schedule_chronobus_upload'))
        self.assertEqual(response.status_code, 200)

        # Post the file
        with open('entries/tests/data/test_schedule.html', 'rb') as schedule_file:
            response = client.post(
                reverse('admin:entries_schedule_chronobus_upload'),
                {
                    'date_effective': '2018-09-01',
                    'published': 'True',
                    'chronobus_file': schedule_file,
                })

        # Should redirect to schedule list in admin
        self.assertEqual(response.status_code, 302)
        
        # Should create a schedule with section and entries
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Schedule.objects.first().scheduleentrysection_set.count(), 1)
        self.assertEqual(Schedule.objects.first().scheduleentrysection_set.first().scheduleentry_set.count(), 2)

        # Should render the schedule on the main page
        response = client.get(reverse('entry-index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(Schedule.objects.first()))
