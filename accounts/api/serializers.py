from rest_framework import fields, serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, password_validation

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
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