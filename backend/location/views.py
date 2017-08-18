from rest_framework import viewsets, mixins
from rest_framework.response import Response

from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from location.models import Location
from core.serializers import UserSerializer
from location.serializers import LocationSerializer

from location.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

User = get_user_model()


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

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
        serializer = self.get_serializer(nearby, many=True)

        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })


class LocationUnavailable(APIException):
    status_code = 404
    default_detail = 'Location not found. Please update location info.'
    default_code = 'location_not_found'
