from core.models import User, Language
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'language',)

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)

        user.set_password(make_password(validated_data['password']))
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'email', 'display_name', 'about_me', 'age', 'height',
                  'weight', 'ethnicity', 'body_type', 'position', 'rel_status',
                  'hiv_status', 'hiv_test_date',)


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'lang_name',)
