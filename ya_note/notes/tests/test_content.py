from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNotePage(TestCase):

    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        all_notes = [
            Note(
                title=f'Новость{index}',
                text='Текст',
                author=cls.author,
                slug=f'note-{index}'
            )
            for index in range(10)
        ]
        Note.objects.bulk_create(all_notes)

    def test_context_notes_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        first_note = object_list[0]
        self.assertIn(first_note, object_list)

    def test_note_not_in_list_for_different_users(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, 0)

    def test_note_in_list_for_author(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, 10)


class TestAddAndEditPage(TestCase):
    """Класс, проверяющий передачу форм на страницы add и edit."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_form(self):
        self.client.force_login(self.author)
        urls = (
            ('notes:edit', (self.notes.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
