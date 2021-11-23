from rest_framework import fields, serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name','last_name','email',]
    
    def update(self, instance, validated_data):
        try:
            instance.username = validated_data['username']
        except KeyError:
            pass
        try:
            instance.first_name = validated_data['first_name']
        except KeyError:
            pass
        try:
            instance.last_name = validated_data['last_name']
        except KeyError:
            pass
        try:
            instance.email = validated_data['email']
        except KeyError:
            pass
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'])
        user.set_password(validated_data["password"])                                
        return user
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()
  class Meta:
        model = User
        fields = ["username", "email","password"]