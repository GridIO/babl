from django.contrib.gis.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.measure import D
from django.contrib.gis.geos import *
from geopy.distance import distance
from operator import itemgetter


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    point = models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return '%s was at (%s) on %s.' % (
            self.user.get_short_name(), self.point,
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )

    def get_distance(self, location2):
        """
        Get distance between self and a separate location object

        Inputs:
        - location2: Location object other user

        Returns: float representing distance between two Location objects
        """
        return distance(self.point, location2.point).km

    def get_near(self):
        """
        Get most recent location events within 20 km radius of self.

        # Inputs:
        # - offset (optional): offsets the returned list by 60; 0 by default

        Returns: queryset containing matching User objects
        """
        objects = Location.objects \
            .exclude(user=self.user) \
            .exclude(user__in=self.user.blocked_users.all()) \
            .filter(point__distance_lte=(self.point, D(km=20))) \
            .order_by('user', '-timestamp').distinct('user')

        return [obj.user for obj in objects]
