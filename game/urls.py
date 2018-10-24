from django.urls import path
from .views import *

urlpatterns = [
    path('', TitleScreenView.as_view(), name='title_screen'),
    path('<int:screen_id>/', GameScreenView.as_view(), name='screen'),
    path('game/', GameView.as_view(), name='game'),
    path('choose_character/', ChooseCharacterView.as_view(), name='choose_character'),
    path('character/', CharacterView.as_view(), name='character'),
    path('graph/', graph, name='graph'),
    path('graph/add/<int:source_id>/', AddRouteView.as_view(), name='add_route'),
]
