from django.contrib import admin
from location.models import Location


class LocationAdmin(admin.ModelAdmin):

    class Meta:
        model = Location
        fields = ('user', 'coords', 'timestamp',)


admin.site.register(Location, LocationAdmin)
