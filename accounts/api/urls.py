from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url


from .views import (
    RegisterApi,
    LoginApi,
    LoginView,
    UserApi,
    login_view_api,
    user_api_update_view,
)
from knox import views as knox_views


urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterApi.as_view(), name='register-api'),
    path('auth/login', LoginView.as_view(), name='login-api'),
    path('auth/logout', knox_views.LogoutView.as_view(), name='logout-api'),
    path('auth/user', UserApi.as_view(), name='user-api'),
    path('update', user_api_update_view)
]