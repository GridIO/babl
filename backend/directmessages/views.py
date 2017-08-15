from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response

from directmessages.models import Message
from directmessages.serializers import MessageGetSerializer
from directmessages.serializers import MessagePostSerializer
from directmessages.serializers import UserSerializer

from directmessages.apps import Inbox
from django.contrib.auth import get_user_model

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """
    API endpoint that lets user get list of conversation partners
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This view should return a list of all the users with which
        the authenticated user has conversations
        """
        users = [
            user.id for user in Inbox.get_conversations(self.request.user)
        ]
        return User.objects.filter(pk__in=users)


class ConversationGetView(generics.ListCreateAPIView):
    """
    API endpoint that lets user see messages in a conversation
    """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MessageGetSerializer

        return MessagePostSerializer

    def get_queryset(self):
        """
        Get messages between user and selected counterparty passed as a param
        """
        user = self.request.user
        counterparty = User.objects.get(
            id=self.request.query_params.get('counterparty_id')
        )

        return Inbox.get_conversation(user, counterparty)
