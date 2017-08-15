from directmessages.models import Message
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'email', 'display_name', 'about_me', 'age', 'height',
                  'weight', 'ethnicity', 'body_type', 'position', 'rel_status',
                  'hiv_status', 'hiv_test_date',)


class MessageGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content',
                  'content_translated', 'sent_at', 'read_at',)


class MessagePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('recipient', 'content',)

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user

        return super(MessagePostSerializer, self).create(validated_data)
