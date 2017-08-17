from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from images.models import ProfileImage
from images.models import ProfileImageOrder

from images.serializers import ProfileImageCreateSerializer
from images.serializers import ProfileImageViewSerializer

from images.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist


class ProfileImageViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileImageCreateSerializer

        return ProfileImageViewSerializer

    def get_queryset(self):
        """
        This view should return a list of all the profile images_views
        with which the authenticated user is associated
        """
        return ProfileImage.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super(ProfileImageViewSet, self).list(request, args, kwargs)
        response.data['order'] = ProfileImageOrder.objects \
                                                  .get(user=request.user) \
                                                  .order

        return response

    @detail_route(methods=['put'])
    def move(self, request, pk=None):
        # get new position and the image id, convert to ints
        new_position = int(request.data['new_position'])
        profile_image_id = int(pk)

        # get the image order object and make the change
        pio = ProfileImageOrder.objects.get(user=request.user)
        pio.move(new_position, profile_image_id)

        return self.list(request)
