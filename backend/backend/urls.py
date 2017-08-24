"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from core import views as core_views
from directmessages import views as directmessages_views
from images import views as images_views
from location import views as locations_views

# API registration
router = routers.DefaultRouter()
router.register(r'users', core_views.UserViewSet)
router.register(r'languages', core_views.LanguageViewSet)
router.register(r'profile-images', images_views.ProfileImageViewSet, base_name='profileimage')
router.register(r'conversations', directmessages_views.ConversationViewSet, base_name='conversation')
router.register(r'locations', locations_views.LocationViewSet, base_name='location')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^media/', include('images.urls')),
    url(r'^media/', include('directmessages.urls')),
    url(r'^login/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
