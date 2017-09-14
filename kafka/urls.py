from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', Homepage.as_view()),
    url(r'^sessie/(?P<slug>[^/]+)/$', Session.as_view(), name='session'),
    url(r'^admin/', admin.site.urls),
]
