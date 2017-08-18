from rest_framework import serializers

from directmessages.models import Message


class MessageGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'message_type',
                  'sender_content', 'recipient_content', 'image',
                  'sent_at', 'read_at',)


class MessagePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('recipient', 'message_type', 'sender_content', 'image',)

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user

        return super(MessagePostSerializer, self).create(validated_data)
