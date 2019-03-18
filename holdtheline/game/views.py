from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Game, Hand, Lanes, Lane, Deck, Player, Card
from .permissions import IsUser, IsSuperUser
from .serializers import GameCreateSerializer, TableSerializer
from .serializers import WallhackGameSerializer, PlayerSerializer, LanesSerializer, LaneSerializer
from .serializers import HandSerializer, DeckSerializer, CardSerializer, GameSerializer



############# Admin ViewSets #################

class WallhackViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = WallhackGameSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminGamesViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminPlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminPlayerCreateSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    ordering_fields = ('id',)
    permission_classes = (IsAdminUser,)


class AdminLanesViewSet(viewsets.ModelViewSet):
    queryset = Lanes.objects.all()
    serializer_class = LanesSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminLaneViewSet(viewsets.ModelViewSet):
    queryset = Lane.objects.all()
    serializer_class = LaneSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminHandViewSet(viewsets.ModelViewSet):
    queryset = Hand.objects.all()
    serializer_class = HandSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminDeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


class AdminCardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    ordering_fields = ('-id',)
    permission_classes = (IsAdminUser,)


############### Game ViewSets ################

class GamesViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    ordering_fields = ('-id',)
    permission_classes = (AllowAny,)


class GameCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = Game.objects.all()
    serializer_class = GameCreateSerializer
    permission_classes = (AllowAny,)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = TableSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsSuperUser,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsUser,)
        return super(self.__class__, self).get_permissions()


class HandViewSet(viewsets.ModelViewSet):
    queryset = Hand.objects.all()
    serializer_class = HandSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsSuperUser,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsUser,)
        return super(self.__class__, self).get_permissions()
