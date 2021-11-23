from rest_framework import serializers
from django.conf import settings
from main.models import Book, Comment
from readers.serializers import PublicProfileSerializer
BOOK_ACTIONS = settings.BOOK_ACTIONS

class BookActionSerializer(serializers.Serializer):
	body = serializers.CharField(allow_blank=True, required=False)
	title = serializers.CharField(allow_blank=True, required=False)
	discription = serializers.CharField(allow_blank=True, required=False)
	id = serializers.IntegerField(required=False)
	action = serializers.CharField()

	def validate_action(self, value):
		value = value.lower().strip()
		if not value in BOOK_ACTIONS:
			raise serializers.ValidationError("There was an error while proccessing that action.")
		return value

class BookSerializer(serializers.ModelSerializer):
	author = PublicProfileSerializer(source='author.userprofile', read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	has_liked = serializers.SerializerMethodField(read_only=True)
	is_me = serializers.SerializerMethodField(read_only=True)
	# parent = StatusCreateSerializer(read_only=True)
	# img = serializers.SerializerMethodField()

	class Meta:
		model = Book
		fields = ['is_me','has_liked','author','id', 'body',  'title', 'discription', 'likes', 'date_added','date_updated']

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
		print(request)
		if request:
			user = request.user
			has_liked = user in  obj.likes.all()
		return has_liked

	def get_body(self,obj):
		body = obj.body
		if obj.is_reply:
			body = obj.parent.body
		return obj.body