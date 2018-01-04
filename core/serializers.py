from django.conf import settings
from rest_framework import serializers
from django.utils._os import safe_join

from location.models import Location
from images.models import ProfileImage
from images.models import get_images
from images.serializers import ProfileImageViewSerializer

from core.models import User, Language
from django.contrib.auth.hashers import make_password

from directmessages.apps import Inbox


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

    images = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    most_recent_message = serializers.SerializerMethodField()
    date_of_last_contact = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'url', 'display_name', 'about_me', 'age', 'height',
                  'weight', 'ethnicity', 'body_type', 'position', 'rel_status',
                  'hiv_status', 'hiv_test_date', 'images', 'distance',
                  'most_recent_message', 'date_of_last_contact',)

    def get_distance(self, user2, *args, **kwargs):
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

    def get_most_recent_message(self, user2, *args, **kwargs):
        user1 = self.context['request'].user

        try:
            msg = Inbox.get_most_recent_message(user1, user2)
        except IndexError:
            return None

        if msg.message_type == 'txt':
            if msg.sender == user1:
                message_sample = msg.sender_content
            else:
                message_sample = msg.recipient_content
        elif msg.message_type == 'img':
            message_sample = 'Image'

        return message_sample

    def get_date_of_last_contact(self, user2, *args, **kwargs):
        user1 = self.context['request'].user

        try:
            return Inbox.get_date_of_last_contact(user1, user2)
        except IndexError:
            return None

    def get_images(self, user, *args, **kwargs):

        try:
            primary = ProfileImage.objects.get(user=user, primary=True)
        except ProfileImage.DoesNotExist:
            return []

        images = [
            img for img in get_images(primary)
            if img.status != 'PEN'
            or (img.status == 'PEN' and user == self.context['request'].user)
        ]

        return ProfileImageViewSerializer(images, many=True, context={'request': self.context['request']}).data


class UserReadOnlySerializer(UserSerializer):

    ethnicity = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    rel_status = serializers.SerializerMethodField()
    hiv_status = serializers.SerializerMethodField()

    def get_ethnicity(self, obj):
        return obj.get_ethnicity_display()

    def get_body_type(self, obj):
        return obj.get_body_type_display()

    def get_position(self, obj):
        return obj.get_position_display()

    def get_rel_status(self, obj):
        return obj.get_rel_status_display()

    def get_hiv_status(self, obj):
        return obj.get_hiv_status_display()


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'lang_name',)
