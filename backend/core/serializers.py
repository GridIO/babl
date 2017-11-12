from rest_framework import serializers

from location.models import Location
from images.models import ProfileImage
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

    distance = serializers.SerializerMethodField()
    most_recent_message = serializers.SerializerMethodField()
    date_of_last_contact = serializers.SerializerMethodField()

    # images = ProfileImageViewSerializer(many=True, read_only=True)
    # images = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'email', 'display_name', 'about_me', 'age', 'height',
                  'weight', 'ethnicity', 'body_type', 'position', 'rel_status',
                  'hiv_status', 'hiv_test_date', 'distance', 'most_recent_message',
                  'date_of_last_contact',)# 'images')

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

    # def get_images(self, user, *args):
    #     order = ProfileImageOrder.objects.get(user=user).order
    #
    #     images = ProfileImage.objects.filter(id__in=order)
    #
    #     images = ProfileImageViewSerializer(images, many=True, read_only=True)
    #
    #     print(images)
    #
    #     return images.data


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('id', 'lang_code', 'lang_name',)
