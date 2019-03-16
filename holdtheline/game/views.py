from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Game, Card, CardLocation, Player, Flag
from .serializers import GameCreateSerializer, GameUpdateSerializer, GameViewSerializer


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