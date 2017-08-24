from django.conf import settings
from django.views.static import serve
from django.utils._os import safe_join

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from images.models import ProfileImage
from images.models import ProfileImageOrder

from images.serializers import ProfileImageCreateSerializer
from images.serializers import ProfileImageViewSerializer

from images.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from core.exceptions import UserUnavailable

from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileImageViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
    List all ProfileImage objects that belong to current user.

    retrieve:
    List all ProfileImage objects for user with id pk, omits all pending and rejected images.

    create:
    Create a new ProfileImage object for current user. Automatically assigned 'pending' as status value.

    destroy:
    Delete an existing ProfileImage object belonging to current user.
    """

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
        response = super(ProfileImageViewSet, self).list(self, args, kwargs)
        response.data['order'] = [item for item in ProfileImageOrder.objects.get(user=request.user).order]

        return response

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise UserUnavailable

        images = ProfileImage.objects.filter(user=user).exclude(status__in=['REJ', 'PEN'])

        page = self.paginate_queryset(images)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

        else:
            serializer = self.get_serializer(images, many=True)
            response = Response(serializer.data)

        image_ids = [img.id for img in images]
        response.data['order'] = [item for item in ProfileImageOrder.objects.get(user=user).order if item in image_ids]

        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        if User.objects.get(id=pk) != request.user:
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        image_id = request.data.get('imageId')

        if not image_id:
            return Response({'detail': 'Please include imageId in request body.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = ProfileImage.objects.get(id=image_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        image.delete()
        return Response({'detail': 'Image successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['put'])
    def move(self, request, pk=None):
        # get new position and the image id, convert to ints
        new_position = int(request.data['new_position'])
        profile_image_id = int(pk)

        # get the image order object and make the change
        pio = ProfileImageOrder.objects.get(user=request.user)
        pio.move(new_position, profile_image_id)

        return self.list(request)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile_image_serve(request, user_id, uuid):

    path = 'profile_images/user_%s/%s.jpg' % (user_id, uuid)

    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['X-Accel-Redirect'] = safe_join(settings.MEDIA_ROOT, path)

    return response
