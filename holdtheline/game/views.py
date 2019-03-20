from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Game, Lanes, Lane, Deck, Player, Card
from .permissions import IsUser, IsSuperUser
from .serializers import GameCreateSerializer, GameSerializer, GameStartSerializer, GameFullSerializer
from .serializers import PlayerSerializer, GamePlayerSerializer
from .serializers import GameLanesSerializer, GameLanesLaneSerializer
from .serializers import GameDeckSerializer, GameDeckCardSerializer
from .serializers import CardSerializer
from .serializers import TableSerializer


############### Game ViewSets ################

## Game
##

class GameBriefViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    ordering_fields = ('-id',)
    permission_classes = (AllowAny,)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameFullSerializer


class GameCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = Game.objects.all()
    serializer_class = GameCreateSerializer
    permission_classes = (AllowAny,)


class GameStartViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameStartSerializer

## Player
##

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class PlayerCreateViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    ordering_fields = ('id',)
    permission_classes = (IsAdminUser,)


class GamePlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = GamePlayerSerializer
    ordering_fields = ('id',)
    permission_classes = (AllowAny,)

    def list(self, request, game=None):
        queryset = Game.objects.filter(id=game).values('player1', 'player2', 'player3', 'player4')[0]
        queryset = Player.objects.filter(Q(id=queryset['player1']) |
                                         Q(id=queryset['player2']) |
                                         Q(id=queryset['player3']) |
                                         Q(id=queryset['player4']))
        serializer = GamePlayerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, game=None, pk=None):
        queryset = Player.objects.get(id=pk)
        serializer = GamePlayerSerializer(queryset, context={'request': request})
        return Response(serializer.data)

## Lanes
##

class GameLanesViewSet(viewsets.ModelViewSet):
    queryset = Lanes.objects.all()
    serializer_class = GameLanesSerializer
    ordering_fields = ('id',)
    permission_classes = (IsAdminUser,)

    def list(self, request, pk=None):
        lanes = Game.objects.get(id=pk).lanes
        queryset = Lanes.objects.get(id=lanes.pk)
        serializer = GameLanesSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class LaneViewSet(viewsets.ModelViewSet):
    queryset = Lanes.objects.all()
    serializer_class = GameLanesLaneSerializer
    ordering_fields = ('id',)
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk=None):
        queryset = Lane.objects.get(id=pk)
        serializer = GameLanesLaneSerializer(queryset, context={'request': request})
        return Response(serializer.data)

## Deck
##

class GameDeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = GameDeckSerializer
    ordering_fields = ('is_played', '-player_fk')
    permission_classes = (IsAdminUser,)

    def list(self, request, pk=None):
        queryset = Deck.objects.filter(game_fk=pk)
        serializer = GameDeckSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = GameDeckCardSerializer
    ordering_fields = ('id',)
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk=None):
        queryset = Deck.objects.get(id=pk)
        serializer = GameDeckCardSerializer(queryset, context={'request': request})
        return Response(serializer.data)

## Card
##

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    ordering_fields = ('id',)
    permission_classes = (AllowAny,)


##### Player viewsets #####

class TableViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = TableSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsSuperUser,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsUser,)
        return super(self.__class__, self).get_permissions()
