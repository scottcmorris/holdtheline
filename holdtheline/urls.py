from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
from .game.views import GameBriefViewSet, GameCreateViewSet, GameStartViewSet, GameViewSet
from .game.views import PlayerViewSet, PlayerCreateViewSet, GamePlayerViewSet
from .game.views import GameLanesViewSet, LaneViewSet
from .game.views import GameDeckViewSet, DeckViewSet
from .game.views import CardViewSet
from .game.views import TableViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'table', TableViewSet)
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)


urlpatterns = [
    ## Default Django urls
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## Games:   /api/v1/game
    path('api/v1/game', GameBriefViewSet.as_view({'get': 'list'}), name='game-list'),
    path('api/v1/game/create', GameCreateViewSet.as_view({'post': 'create'}), name='game-create'),
    path('api/v1/game/<int:pk>/start', GameStartViewSet.as_view({'get': 'list', 'put': 'update'}), name='game-start'),
    path('api/v1/game/<int:pk>', GameViewSet.as_view({'get': 'retrieve'}), name='game-detail'),


    ## Players: /api/v1/players
    path('api/v1/player', PlayerViewSet.as_view({'get': 'list'}), name='player-list'),
    path('api/v1/player/create', PlayerCreateViewSet.as_view({'get': 'list', 'post': 'create'}), name='player-create'),
    path('api/v1/player/<int:pk>', PlayerViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='player-detail'),
    ##          /api/v1/game/#/players
    path('api/v1/game/<int:game>/player', GamePlayerViewSet.as_view({'get': 'list'}), name='game-player-list'),
    path('api/v1/game/<int:game>/player/<int:pk>', GamePlayerViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='game-player-detail'),


    ## Lanes:   /api/v1/game/#/lanes
    path('api/v1/game/<int:pk>/lanes', GameLanesViewSet.as_view({'get': 'list'}), name='game-lanes-list'),


    ## Lane:    /api/v1/lane/#
    path('api/v1/lane/<int:pk>', LaneViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='lane-detail'),


    ## Card:    /api/v1/card
    path('api/v1/card', CardViewSet.as_view({'get': 'list'}), name='card-list'),


    ## Deck:    /api/v1/game/#/deck
    path('api/v1/game/<int:pk>/deck', GameDeckViewSet.as_view({'get': 'list'}), name='game-deck-list'),
    ##          /api/v1/deck/#
    path('api/v1/deck/<int:pk>', DeckViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='deck-detail'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
