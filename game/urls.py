from django.urls import path
from .views import *

urlpatterns = [
    path('', TitleScreenView.as_view(), name='title_screen'),
    path('<int:screen_id>/', GameScreenView.as_view(), name='screen'),
    path('play/', GameView.as_view(), name='game'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('graph/', graph, name='graph'),
    path('graph/add/<int:source_id>/', AddRouteView.as_view(), name='add_route'),
]
