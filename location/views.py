from rest_framework import viewsets, mixins
from rest_framework.response import Response

from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from location.models import Location
from core.serializers import UserSerializer
from location.serializers import LocationSerializer

from operator import itemgetter

from location.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

User = get_user_model()


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
    Return a list of Users, ordered by closest to farthest, based on logged in user's most recent location

    create:
    Create a new Location instance; must contain a Point object in str form
    e.g. POINT(-73.985588 40.758064) --> Times Square, NYC
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action == 'create':
            return LocationSerializer

    def list(self, request):

        try:
            loc = Location.objects.filter(user=request.user) \
                          .latest('timestamp')

        except ObjectDoesNotExist:
            raise LocationUnavailable

        nearby = loc.get_near()

        # start pagination
        page = self.paginate_queryset(nearby)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # create response and order people by distance
            response = self.get_paginated_response(serializer.data)
            response.data['results'].sort(key=itemgetter('distance'))

            return response
        # end pagination

        serializer = self.get_serializer(nearby, many=True)

        return Response(serializer.data)


class LocationUnavailable(APIException):
    status_code = 404
    default_detail = 'Location not found. Please update location info.'
    default_code = 'location_not_found'
