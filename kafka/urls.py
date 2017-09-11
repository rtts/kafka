from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', Homepage.as_view()),
    url(r'^admin/', admin.site.urls),
]
