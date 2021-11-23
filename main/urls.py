from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('main.api.urls')),
    path('', include('main.commentsapi.urls')),
]