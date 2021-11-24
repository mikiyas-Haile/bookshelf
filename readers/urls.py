from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url

from .views import   (
      current_user_api_view,
      profile_detail_api_view,
      user_follow_view, 
      all_user_profile_list_view,
      api_my_followers,
      profile_api_update_view,
      UsersAPIView,
       )

from . import views

urlpatterns = [
   # REST API 
   path('api/profile/settings', profile_api_update_view),
   path('api/<str:user>/followers', api_my_followers),
   path("api/<str:username>", profile_detail_api_view),
   path("api/profile/me", current_user_api_view),
   path("api/all/profiles", all_user_profile_list_view),
   path("users", UsersAPIView.as_view()),
   path("api/<str:username>/follow", user_follow_view),
]