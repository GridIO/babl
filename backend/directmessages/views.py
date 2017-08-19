from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from core.exceptions import UserUnavailable

from directmessages.models import Message
from directmessages.serializers import MessageGetSerializer
from directmessages.serializers import MessagePostSerializer
from core.serializers import UserSerializer

from directmessages.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from directmessages.apps import Inbox
from django.contrib.auth import get_user_model

User = get_user_model()


class ConversationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
    Get list of User objects sorted from nearest to farthest from current user.

    retrieve:
    Retrieve all messages between current user and another user specified by their pk.

    create:
    Creates a new message to be sent to another user from current user.
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action == 'retrieve':
            return MessageGetSerializer
        if self.action == 'create':
            return MessagePostSerializer

        # return MessageGetSerializer

    def get_queryset(self):
        """

        """
        users = [
            user.id for user in Inbox.get_conversations(self.request.user)
        ]
        return User.objects.filter(pk__in=users)

    def retrieve(self, request, pk=None, format=None):
        user = self.request.user
        try:
            counterparty = User.objects.get(id=pk)

        except ObjectDoesNotExist:
            raise UserUnavailable

        if counterparty not in user.blocked_users.all():
            messages = Inbox.get_conversation(user, counterparty)
        else:
            raise UserUnavailable

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
