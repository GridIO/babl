from rest_framework import serializers

from location.models import Location
from core.models import User, Language
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

    distance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'email', 'display_name', 'about_me', 'age', 'height',
                  'weight', 'ethnicity', 'body_type', 'position', 'rel_status',
                  'hiv_status', 'hiv_test_date', 'distance',)

    def get_distance(self, user2):

        user1 = self.context['request'].user

        if user1 != user2:
            locations = Location.objects.filter(user__in=[user1, user2]) \
                                .order_by('user', '-timestamp') \
                                .distinct('user')

            try:
                return locations[0].get_distance(locations[1])
            except IndexError:
                return None

        return 0.0


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'lang_name',)
