from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url


from .views import (
       RegisterView,
       LoginView,
       LogoutView,
       CustomAuthToken,
)


urlpatterns = [
   path('api/', include('accounts.api.urls')),
   path('api-token-auth/', CustomAuthToken.as_view()),
   path('register/', RegisterView, name="register"),
   path('login/', LoginView, name="login"),
   path('logout/', LogoutView, name="logout"),
]