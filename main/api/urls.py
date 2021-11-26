from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import (
    BookListView,
    BookActionView,
    BookDetailView,
    django_csrf,
)
urlpatterns = [
    path("csrf",django_csrf,name='csrf_token'),
    path('', BookListView.as_view()),
    path('action', BookActionView),
    path('<int:book_id>', BookDetailView),
]