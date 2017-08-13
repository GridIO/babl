from django.contrib import admin
from images.models import ProfileImage


class ProfileImageAdmin(admin.ModelAdmin):

    class Meta:
        model = ProfileImage
        fields = ('user', 'image',)

    def get_readonly_fields(self, request, obj=None):
        return ('order',)


admin.site.register(ProfileImage, ProfileImageAdmin)
