from django.conf import settings
from django.views.static import serve
from django.utils._os import safe_join
from django.http import Http404

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from images.models import ProfileImage
from images.models import get_images

from images.serializers import ProfileImageCreateSerializer
from images.serializers import ProfileImageViewSerializer

from images.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileImageViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    GET /profile-images/:
    List all ProfileImage objects that belong to current user.

    POST /profile-images/:
    Create a new ProfileImage object for current user. Automatically assigned 'pending' as status value.

    GET /profile-images/{pk}/:
    Get a single serialized profile image by its ID number.

    DELETE /profile-images/{pk}/:
    Delete an existing ProfileImage object belonging to current user.

    PATCH /profile-images/{pk}/move/:
    Change a ProfileImage's order to index value provided in body; must be owner of image.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = ProfileImage.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileImageCreateSerializer

        return ProfileImageViewSerializer

    def list(self, request, *args, **kwargs):
        queryset = get_images(ProfileImage.objects.get(user=request.user, primary=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        if ProfileImage.objects.get(id=pk).user != request.user:
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            image = ProfileImage.objects.get(id=pk)
        except ProfileImage.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        image.delete()
        return Response({'detail': 'Image successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['patch'])
    def move(self, request, pk=None):
        # get desired new index
        index = request.data.get('index')
        if index is None:
            raise Response({
                'detail': 'You must indicate an index value to move image.'}, status=status.HTTP_400_BAD_REQUEST
            )

        # check to make sure that image exists, raise 404 if not found
        try:
            image = ProfileImage.objects.get(id=pk)
        except ProfileImage.DoesNotExist:
            raise Http404

        # ensure that user owns the image
        if request.user != image.user:
            return Response({'detail': 'User must be owner of image to move.'}, status=status.HTTP_401_UNAUTHORIZED)

        # move image to desired index
        image.move(int(index))

        return Response({'detail': 'Image successfully moved.'}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile_image_serve(request, user_id, uuid):

    path = 'profile_images/user_%s/%s.jpg' % (user_id, uuid)

    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['X-Accel-Redirect'] = safe_join(settings.MEDIA_ROOT, path)

    return response
