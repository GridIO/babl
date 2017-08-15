from rest_framework import viewsets, mixins, pagination

from core.models import User, Language
from core.serializers import SignUpSerializer
from core.serializers import UserSerializer
from core.serializers import LanguageSerializer

from core.permissions import IsOwnerOrReadOnly
from core.permissions import IsAdminOrReadOnly
from core.permissions import IsCreationOrIsAuthenticated
from rest_framework.permissions import IsAuthenticated


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    permission_classes = (IsOwnerOrReadOnly, IsCreationOrIsAuthenticated,)

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
    API endpoint that allows languages to be viewed as a list
    """
    permission_classes = (IsAuthenticated,)

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
