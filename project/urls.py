from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

import kafka.urls
import game.urls

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('', include(kafka.urls)),
    #path('game/', include(game.urls)),
    path('ddw/', include(game.urls)),
]
