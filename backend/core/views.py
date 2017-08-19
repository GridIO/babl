from rest_framework import viewsets, mixins, pagination

from core.models import User, Language
from core.serializers import SignUpSerializer
from core.serializers import UserSerializer
from core.serializers import LanguageSerializer

from core.permissions import IsSelfOrReadOnly
from core.permissions import IsCreationOrIsAuthenticated
from rest_framework.permissions import IsAuthenticated


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    retrieve:
    Get the primary information of a user.

    update:
    Update the primary information of current user.

    create:
    Create a new user object.
    """
    permission_classes = (IsSelfOrReadOnly, IsCreationOrIsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        else:
            return UserSerializer


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
