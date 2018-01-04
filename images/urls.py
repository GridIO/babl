from django.conf.urls import url
from images.views import profile_image_serve


urlpatterns = [
    url(r'^profile_images/user_(?P<user_id>\d+)/(?P<uuid>[0-9a-f-]+).jpg$', profile_image_serve, name='profile_image_service'),
]
