from django.urls import path
from .views import *

urlpatterns = [
    path('', GameView.as_view(), name='game'),
    path('start/', ChooseCharacterView.as_view(), name='choose_character'),
    path('graph/', graph),
    path('graph/edit/', graph, name='graph', kwargs={'edit': True}),
    path('graph/add/<int:source_id>/', add_screen, name='add_screen'),
    path('graph/add/<int:source_id>/<int:target_id>/', add_screen, name='add_screen'),
]
