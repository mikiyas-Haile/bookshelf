from rest_framework.pagination import PageNumberPagination

from django.shortcuts import render
from rest_framework import response
from django.db.models.aggregates import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from rest_framework.serializers import Serializer

from .serializers import PublicProfileSerializer
from .models import UserProfile
from rest_framework import generics
from rest_framework import filters
User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

class UsersAPIView(generics.ListCreateAPIView):
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    filter_backends = (filters.SearchFilter,)
    queryset = UserProfile.objects.annotate(num_likess=Count('followers')).order_by('-num_likess')
    serializer_class = PublicProfileSerializer

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def user_follow_view(request,username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username)
    if me.username == username:
        my_followers = me.userprofile.followers.all()
        return Response({"count": my_followers.count()}, status=200)
    if not other_user_qs.exists():
        return Response({}, status=404)
    other =  other_user_qs.first()
    profile = other.userprofile
    data = request.data or {}
    action = data.get("action")
    if action == "follow":
        profile.followers.add(me)
    elif action == 'unfollow':
        profile.followers.remove(me)
    else:
        pass
    current_followers_qs = profile.followers.all()
    return Response({"count": current_followers_qs.count()}, status=200)

@api_view(['PUT',])
def profile_api_update_view(request):
    qs = UserProfile.objects.filter(user__username=request.user)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if request.method == 'PUT':
        serializer = PublicProfileSerializer(obj,data=request.data, context={"request":request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Profile has been successfully upated."
            return Response(serializer.data,200)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def all_user_profile_list_view(request, *args, **kwargs):
    qs = UserProfile.objects.all()
    serializer = PublicProfileSerializer(qs,many=True, context={"request":request})
    return Response(serializer.data, 200)


@api_view(["GET"])
def api_my_followers(request, user,*args, **kwargs):
    user = UserProfile.objects.filter(user__username=user).first()
    followers = user.followers.all()
    followings = user.user.following.all()
    followerss = []
    followingss = []
    if followings.exists():
        for following in followings:
            following = UserProfile.objects.filter(user__username=following).first()
            followingss.append(following)
    if followers.exists():
        for follower in followers:
            follower = UserProfile.objects.filter(user__username=follower).first()
            followerss.append(follower)
    follower_serializer = PublicProfileSerializer(followerss, many=True, context={"request":request})
    following_serializer = PublicProfileSerializer(followingss, many=True, context={"request":request})
    return Response({"Followers": follower_serializer.data, "Following":following_serializer.data }, 200)


@api_view(["GET"])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = UserProfile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail":"User not found. Check the username and enter it properly."}, status=404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(instance=profile_obj, context={"request":request} )
    return Response(data.data, status=200)

@api_view(["GET"])
def current_user_api_view(request, *args, **kwargs):
    user = request.user.username
    qs = UserProfile.objects.filter(user__username=user)
    if not qs.exists():
        return Response({"detail":"You aren't Authenticated."}, status=400)
    profile_obj = qs.first()
    context ={
        "request": request,
        "current_user": profile_obj
    }
    data = PublicProfileSerializer(instance=profile_obj, context=context)
    return Response(data.data, status=200)