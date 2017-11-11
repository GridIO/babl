from django.conf import settings
from django.views.static import serve
from django.utils._os import safe_join
from django.http import Http404

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED

from directmessages.models import Message
from directmessages.serializers import MessageGetSerializer
from directmessages.serializers import MessagePostSerializer

from directmessages.exceptions import RecipientCantBeSelf
from directmessages.exceptions import MustHaveRecipient

from directmessages.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from directmessages.apps import Inbox
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    GET /messages/?recipient={user_id}:
    Get all messages between user and recipient; must have recipient

    POST /messages/?recipient={user_id}:
    Send a message from user to recipient; must have recipient
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MessagePostSerializer

        return MessageGetSerializer

    def list(self, request, *args, **kwargs):
        recipient = recipient_checker(request)

        queryset = Inbox.get_conversation(request.user, recipient)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        recipient = recipient_checker(request)

        serializer = self.get_serializer(data=request.data)
        serializer.context['recipient'] = recipient
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def message_image_serve(request, user1_id, user2_id, uuid):

    user_id = request.user.id

    if user_id not in (int(user1_id), int(user2_id)):
        raise Http404

    path = 'message_images/user_%s/user_%s/%s.jpg' % (user1_id, user2_id, uuid)

    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['X-Accel-Redirect'] = safe_join(settings.MEDIA_ROOT, path)

    return response


# HELPER FUNCTIONS

def recipient_checker(request):
    """
    Check that recipient behaves in expected way

    :param request: HTTP request to be checked
    :return: returns User object if all checks successful
    """
    recipient_id = request.GET.get('recipient')

    # sender and recipient must be specified in url
    if recipient_id is None:
        raise MustHaveRecipient

    # sender and recipient can't be the same user
    if int(recipient_id) == request.user.id:
        raise RecipientCantBeSelf

    # check if recipient exists, otherwise raise 404
    try:
        recipient = User.objects.get(id=recipient_id)
    except User.DoesNotExist:
        raise Http404

    # check if the users blocked one another, if so raise 404
    if recipient_id in request.user.blocked_users.all():
        raise Http404

    return recipient
