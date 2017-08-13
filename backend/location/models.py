from django.contrib.gis.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.measure import D
from django.contrib.gis.geos import *
from geopy.distance import distance
from operator import itemgetter


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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

    def get_near(self, offset=0):
        """
        Get most recent location events within 20 km radius of self.

        Inputs:
        - offset (optional): offsets the returned list by 60; 0 by default

        Returns: array with dicts containing two elements:
        - user:     User object for nearby user
        - distance: GeoPy Distance object repr how far user is from self
        """
        obj = Location.objects \
            .exclude(user=self.user) \
            .filter(point__distance_lte=(self.point, D(km=20))) \
            .order_by('user', '-timestamp').distinct('user')

        results = sorted([{
            'user': i.user,
            'distance': distance(self.point, i.point)
        } for i in obj], key=itemgetter('distance'))

        return results[60 * offset: 60 * (offset + 1)]
