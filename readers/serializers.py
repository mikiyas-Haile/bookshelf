from rest_framework import serializers

from .models import UserProfile
from main.models import Book
class PublicProfileSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField(read_only=True)
    books = serializers.SerializerMethodField(read_only=True)
    birthday = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    # pfp_url = serializers.SerializerMethodField()
    is_my_profile = serializers.SerializerMethodField(read_only=True)
    request_user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'books',
            'verified',
            'birthday',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'pfp_url',
            'bio',
            'insta',
            'twitter',
            'tiktok',
            'youtube',
            'follower_count',
            'following_count',
            'is_following',
            'is_my_profile',
            'request_user',
        ]

    def update(self, instance, validated_data):
        try:
            instance.youtube = validated_data['youtube']
        except KeyError:
            pass
        try:
            instance.twitter = validated_data['twitter']
        except KeyError:
            pass
        try:
            instance.insta = validated_data['insta']
        except KeyError:
            pass
        try:
            instance.bio = validated_data['bio']
        except KeyError:
            pass
        try:
            instance.tiktok = validated_data['tiktok']
        except KeyError:
            pass
        instance.save()
        return instance
    def get_books(self, obj):
        qs = Book.objects.filter(author__username=obj.user.username)
        return qs.count()
    def get_is_my_profile(self, obj):
        is_my_profile = False
        context = self.context
        request = context.get("request")
        current_user = str(context.get("current_user"))
        user = request.user.username
        if user == current_user:
            is_my_profile = True
        return is_my_profile

    def get_verified(self, obj):
        verified = obj.verified
        return verified
    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in  obj.followers.all()
        return is_following

    # def get_pfp_url(self, obj):
    #     try:
    #         return obj.user.userprofile.pfp.url
    #     except ValueError:
    #         return '/media/images/default-pfp_C7ckHUn.png'
    def get_birthday(self, obj):
        return obj.user.userprofile.birthday
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_username(self, obj):
        return obj.user.username
    def get_following_count(self, obj):
        return obj.user.following.count()
    def get_follower_count(self, obj):
        return obj.followers.count()
    def get_request_user(self, obj):
        context = self.context
        request = context.get("request")
        if request:
            request_user = request.user.username
        return request_user

