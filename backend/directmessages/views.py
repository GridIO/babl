from rest_framework import viewsets, mixins, generics
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from directmessages.models import Message
from directmessages.serializers import MessageGetSerializer
from directmessages.serializers import MessagePostSerializer
from directmessages.serializers import UserSerializer

from core.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from directmessages.apps import Inbox
from django.contrib.auth import get_user_model

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """
    API endpoint that lets user get list of conversation partners
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

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
        try:
            counterparty = User.objects.get(
                id=self.request.query_params.get('counterparty_id')
            )
        except ObjectDoesNotExist:
            raise UserUnavailable

        return Inbox.get_conversation(user, counterparty)


class UserUnavailable(APIException):
    status_code = 404
    default_detail = 'User not found. Please provide a valid id.'
    default_code = 'user_not_found'
