from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.http import Http404
from location.exceptions import LocationUnavailable

from core.models import User, Language
from core.serializers import SignUpSerializer
from core.serializers import UserSerializer
from core.serializers import UserReadOnlySerializer
from core.serializers import LanguageSerializer

from core.permissions import IsSelfOrReadOnly
from core.permissions import IsCreationOrIsAuthenticated
from rest_framework.permissions import IsAuthenticated

from location.models import Location
from directmessages.apps import Inbox


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    POST /users/:
    Create a new user object.

    GET /users/{pk}/:
    Get the primary information of a user.

    GET /users/me/:
    Gets the current logged in user's profile.

    PATCH /users/me/:
    Update the primary information of user with id {pk}.

    GET /users/closest/:
    Get the users closest to current user ordered from closest to farthest.

    GET /users/conversations/:
    Get all the conversations that the current user has ordered from most to least recent.
    """
    permission_classes = (IsSelfOrReadOnly, IsCreationOrIsAuthenticated,)

    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):

        print(self.action)

        if self.action == 'create':
            return SignUpSerializer
        else:
            return UserSerializer

    @list_route(methods=['get'])
    def closest(self, request):

        try:
            location = Location.objects.filter(user=request.user.id).latest('timestamp')
            queryset = location.get_near()
        except Location.DoesNotExist:
            raise LocationUnavailable

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(sorted(serializer.data, key=lambda k: k['distance']))

        serializer = self.get_serializer(queryset, many=True)
        return Response(sorted(serializer.data, key=lambda k: k['distance']))

    @list_route(methods=['get'])
    def conversations(self, request):

        conversations = Inbox.get_conversations(User.objects.get(id=request.user.id))

        page = self.paginate_queryset(conversations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                sorted(serializer.data, key=lambda k: k['date_of_last_contact'], reverse=True)
            )

        serializer = self.get_serializer(conversations, many=True)
        return Response(sorted(serializer.data, key=lambda k: k['date_of_last_contact'], reverse=True))

    @list_route(methods=['get'])
    def me(self, request, *args, **kwargs):

        me = [request.user]

        page = self.paginate_queryset(me)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(me, many=True)
        return Response(serializer.data)


class LanguageViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
    list all languages available for translation.

    retrieve:
    retrieve an individual language object.
    """
    permission_classes = (IsAuthenticated,)

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
