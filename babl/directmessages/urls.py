from django.conf.urls import url
from directmessages.views import message_image_serve


urlpatterns = [
    url(r'^message_images/user_(?P<user1_id>\d+)/user_(?P<user2_id>\d+)/(?P<uuid>[0-9a-f-]+).jpg$', message_image_serve, name='message_image_service'),
]
