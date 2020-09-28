from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            print(email)
            try:
                user = User.objects.get(email=email)
            except:
                msg = _('User is not exist')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.check_password(password):
                msg = _('Password is incorrect')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class SignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    @staticmethod
    def save_user(validated_data):
        user = User()
        user.username = validated_data['full_name']
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.is_active = True
        user.is_superuser = False
        user.save()
        return user
