from rest_framework import serializers
from images.models import ProfileImage


class ProfileImageCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ('id', 'image',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(ProfileImageCreateSerializer, self).create(validated_data)


class ProfileImageViewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ('id', 'image', 'status',)
