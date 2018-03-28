from rest_framework import serializers

from location.models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('point',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(LocationSerializer, self).create(validated_data)
