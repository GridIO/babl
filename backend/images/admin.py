from django.contrib import admin
from images.models import ProfileImage
from images.models import ProfileImageOrder


class ProfileImageAdmin(admin.ModelAdmin):

    class Meta:
        model = ProfileImage
        fields = ('user', 'image',)


class ProfileImageOrderAdmin(admin.ModelAdmin):

    class Meta:
        model = ProfileImageOrder
        fields = ('order',)


admin.site.register(ProfileImage, ProfileImageAdmin)
admin.site.register(ProfileImageOrder, ProfileImageOrderAdmin)
