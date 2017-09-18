from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^$', Homepage.as_view()),
    url(r'^sessie/(?P<slug>[^/]+)/$', Session.as_view(), name='session'),
    url(r'^admin/', admin.site.urls),
]
