from rest_framework import serializers
from django.conf import settings
from main.models import Book, Comment
from readers.serializers import PublicProfileSerializer
BOOK_ACTIONS = settings.BOOK_ACTIONS
from main.api.serializers import BookSerializer

class BookCommentActionSerializer(serializers.Serializer):
	body = serializers.CharField(allow_blank=True, required=False)
	id = serializers.IntegerField(required=False)
	action = serializers.CharField()

	def validate_action(self, value):
		value = value.lower().strip()
		if not value in BOOK_ACTIONS:
			raise serializers.ValidationError("There was an error while proccessing that action.")
		return value


class BookCommentCreateSerializer(serializers.ModelSerializer):
	author = PublicProfileSerializer(source='author.userprofile', read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	
	class Meta:
		model = Comment
		fields = ['author','id', 'body', 'likes', 'date_added']

	def get_likes(self, obj):
		return obj.likes.count()

	def validate_body(self, value):
		if len(value)>140:
			raise serializers.ValidationError("Comment too long. Please shorten it.")
		return value

class BookCommentsSerializer(serializers.ModelSerializer):
	book = BookSerializer()
	author = PublicProfileSerializer(source='author.userprofile', read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	has_liked = serializers.SerializerMethodField(read_only=True)
	is_me = serializers.SerializerMethodField(read_only=True)
	parent = BookCommentCreateSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = ['book','is_me','has_liked', 'is_reply', 'parent', 'author','id', 'body', 'likes', 'date_added','date_updated']

	def update(self, instance, validated_data):
		# Update the Foo instance
		instance.body = validated_data['body']
		instance.save()
		return instance


	def get_is_me(self, obj):
		is_me = False
		context = self.context
		request = context.get("request")
		if request:
			user = request.user
			if user == obj.author:
				is_me = True
		return is_me

	def get_likes(self, obj):
		return obj.likes.count()

	def get_has_liked(self, obj):
		has_liked = False
		context = self.context
		request = context.get("request")
		if request:
			user = request.user
			has_liked = user in  obj.likes.all()
		return has_liked

	def get_body(self,obj):
		body = obj.body
		if obj.is_reply:
			body = obj.parent.body
		return obj.body