from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Topic


class LearningLogAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='testpass123')
        self.other = User.objects.create_user('bob', password='testpass123')
        self.topic = Topic.objects.create(owner=self.user, text='Chess')
        self.other_topic = Topic.objects.create(owner=self.other, text='Climbing')
        self.entry = Entry.objects.create(topic=self.topic, text='Study openings.')
        self.other_entry = Entry.objects.create(topic=self.other_topic, text='Use a rope.')

    def test_topics_require_login(self):
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response['Location'])

    def test_topics_are_filtered_by_owner(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertContains(response, 'Chess')
        self.assertNotContains(response, 'Climbing')

    def test_topic_detail_rejects_other_owner(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('learning_logs:topic', args=[self.other_topic.id]))
        self.assertEqual(response.status_code, 404)

    def test_new_topic_sets_owner(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(reverse('learning_logs:new_topic'), {'text': 'Django'})
        topic = Topic.objects.get(text='Django')
        self.assertEqual(topic.owner, self.user)

    def test_edit_entry_rejects_other_owner(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('learning_logs:edit_entry', args=[self.other_entry.id]),
            {'text': 'Changed'},
        )
        self.assertEqual(response.status_code, 404)
        self.other_entry.refresh_from_db()
        self.assertEqual(self.other_entry.text, 'Use a rope.')
