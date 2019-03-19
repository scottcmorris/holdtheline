from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
from .game.views import GameCreateViewSet, GamesViewSet, TableViewSet
from .game.views import WallhackViewSet, AdminPlayerViewSet, AdminGamesViewSet, AdminCardViewSet, AdminDeckViewSet
from .game.views import AdminLanesViewSet, AdminLaneViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'games', GamesViewSet)
router.register(r'table', TableViewSet)
router.register(r'wallhack', WallhackViewSet)
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)


# router.register(r'games/(?P<pk>\d+)/$', GameUpdateViewSet)
# router.register(r'games/create', GameCreateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('api/v1/wallhack$', WallhackViewSet.as_view({'get': 'list'}), name='wallhack'),
    re_path('api/v1/wallhack/card$',
            AdminCardViewSet.as_view({'get': 'list'}), name='wallhack-card-list'),
    re_path('api/v1/wallhack/card/(?P<pk>\d+)$',
            AdminCardViewSet.as_view({'get': 'list', 'put': 'update'}), name='wallhack-card-detail'),
    re_path('api/v1/wallhack/deck$',
            AdminDeckViewSet.as_view({'get': 'list'}), name='wallhack-deck-list'),
    re_path('api/v1/wallhack/deck/create$',
            AdminDeckViewSet.as_view({'get': 'list', 'post': 'create'}), name='wallhack-deck-create'),
    re_path('api/v1/wallhack/deck/(?P<pk>\d+)$',
            AdminDeckViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='wallhack-deck-detail'),
    re_path('api/v1/wallhack/games$',
            AdminGamesViewSet.as_view({'get': 'list', 'post': 'create'}), name='wallhack-games-list'),
    re_path('api/v1/wallhack/games/(?P<pk>\d+)$',
            AdminGamesViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='wallhack-games-detail'),
    re_path('api/v1/wallhack/lane$',
            AdminLaneViewSet.as_view({'get': 'list'}), name='wallhack-lane-list'),
    re_path('api/v1/wallhack/lane/(?P<pk>\d+)$',
            AdminLaneViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='wallhack-lane-detail'),
    re_path('api/v1/wallhack/lanes$',
            AdminLanesViewSet.as_view({'get': 'list'}), name='wallhack-lanes-list'),
    re_path('api/v1/wallhack/lanes/(?P<pk>\d+)$',
            AdminLanesViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='wallhack-lanes-detail'),
    re_path('api/v1/wallhack/player$',
            AdminPlayerViewSet.as_view({'get': 'list'}), name='wallhack-player-list'),
    re_path('api/v1/wallhack/player/create$',
            AdminPlayerViewSet.as_view({'get': 'list', 'post': 'create'}), name='wallhack-player-create'),
    re_path('api/v1/wallhack/player/(?P<pk>\d+)$',
            AdminPlayerViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='wallhack-player-detail'),

                  # re_path('api/v1/games/$', GameViewSet.as_view({'get': 'list'}), name='games-list'),
    # re_path('api/v1/games/(?P<pk>\d+)/$', GameUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='games-update'),
    path('api/v1/games/create/', GameCreateViewSet.as_view({'post': 'create'}), name='games-create'),

                  # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
