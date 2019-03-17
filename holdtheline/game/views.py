from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Game, Hand, Lanes, Lane, Deck,Player
from .serializers import GameCreateSerializer, GameUpdateSerializer, GameViewSerializer, GameSerializer, CardSerializer
from .serializers import PlayerSerializer, LanesSerializer, LaneSerializer


class GameCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = Game.objects.all()
    serializer_class = GameCreateSerializer
    permission_classes = (AllowAny,)


class GameViewSet(
                  # mixins.ListModelMixin,
                  # mixins.RetrieveModelMixin,
                  # mixins.UpdateModelMixin,
                  viewsets.ModelViewSet):

    http_method_names = ['get', 'head']

    queryset = Game.objects.all()
    serializer_class = GameViewSerializer
    permission_classes = (AllowAny,)



class GameUpdateViewSet(
    # mixins.RetrieveModelMixin,
    #                     mixins.UpdateModelMixin,
                         viewsets.ModelViewSet):

    http_method_names = ['get', 'put', 'retrieve', 'head']

    queryset = Game.objects.all()
    serializer_class = GameUpdateSerializer
    permission_classes = (AllowAny,)


class MainViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    ordering_fields = ('-id',)


class LanesViewSet(viewsets.ModelViewSet):
    queryset = Lanes.objects.all()
    serializer_class = LanesSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
