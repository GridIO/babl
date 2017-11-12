from django.contrib import admin
from images.models import ProfileImage


class ProfileImageAdmin(admin.ModelAdmin):

    list_display = ('user', 'image', 'next_image', 'status', 'primary', )
    list_filter = ('status', 'primary',)

    class Meta:
        model = ProfileImage
        fields = ('user', 'image', 'status','primary', 'next_image',)


admin.site.register(ProfileImage, ProfileImageAdmin)
