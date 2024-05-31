import pytest
from django.conf import settings
from datetime import timedelta

from django.test.client import Client

from news.models import News, Comment
from django.utils import timezone


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
    }


@pytest.fixture
def news_10(author):
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}', text='Просто текст.')
        all_news.append(news)
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def comments(author, news):
    all_comments = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
        all_comments.append(comment)
    return all_comments


@pytest.fixture
def id_news_for_args(news):
    return (news.id,)


@pytest.fixture
def id_comment_for_args(comment):
    return (comment.id,)
