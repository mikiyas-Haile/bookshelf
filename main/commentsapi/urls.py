from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import (
    CommentListView,
    BookActionView,
)
urlpatterns = [
    path('<int:book_pk>/comments', CommentListView),
    path('<int:book_pk>/action', BookActionView),
]