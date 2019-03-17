from rest_framework import serializers
from .models import Game, Card, Lane, Lanes, Deck, Hand, Player
from random import shuffle


class GameCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('pk', 'player1',)

    def create(self, validated_data):
        self.create_game(validated_data)
        self.shuffle_deck()

        return self.game

    def create_game(self, validated_data):
        player1 = validated_data.pop('player1')

        self.setup_lanes()

        self.game = Game(player1=player1, lanes=self.lanes)
        self.game.save()

    def setup_lanes(self):
        lanes = [None]
        for i in range(1, 10):
            lane = Lane()
            lane.save()
            lanes.append(lane)

        self.lanes = Lanes(lane1=lanes[1],
                           lane2=lanes[2],
                           lane3=lanes[3],
                           lane4=lanes[4],
                           lane5=lanes[5],
                           lane6=lanes[6],
                           lane7=lanes[7],
                           lane8=lanes[8],
                           lane9=lanes[9])
        self.lanes.save()

    def shuffle_deck(self):
        cards = list(Card.objects.all())
        shuffle(cards)

        for card in cards:
            deck = Deck(game=self.game, card=card)
            deck.save()


class GameViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'


class GameUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('pk', 'player1', 'player2', 'player3', 'player4')

    def update(self, game, validated_data=None):
        if validated_data is not None:
            players = [validated_data.pop('player1'),
                       validated_data.pop('player2'),
                       validated_data.pop('player3'),
                       validated_data.pop('player4')]

            if players:
                for i, player in enumerate(players, start=1):
                    game.set_player(i, player)
                    game.save()
            return game

    def retrieve(self, game, validated_data=None):
        if validated_data is not None:
            return game


class NestedSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop('nested', False)
        super().__init__(*args, **kwargs)
        if nested:
            self.fields.update(
                {'pk': serializers.IntegerField(validators=[])}
            )


class LaneSerializer(NestedSerializer):

    class Meta:
        model = Lane
        fields = [field.name for field in model._meta.fields if not field.primary_key]


class CardSerializer(NestedSerializer):

    class Meta:
        model = Card
        fields = [field.name for field in model._meta.fields if not field.primary_key]


class PlayerSerializer(NestedSerializer):
    hand = serializers.SerializerMethodField('player_hand')

    def player_hand(self, player):
        hand = Hand.objects.filter(player=player, game=self.context.get('game'))
        return list(hand)

    class Meta:
        model = Player
        fields = [field.name for field in model._meta.fields if not field.primary_key] + ['hand']


class LanesSerializer(NestedSerializer):
    lane1 = LaneSerializer()
    lane2 = LaneSerializer()
    lane3 = LaneSerializer()
    lane4 = LaneSerializer()
    lane5 = LaneSerializer()
    lane6 = LaneSerializer()
    lane7 = LaneSerializer()
    lane8 = LaneSerializer()
    lane9 = LaneSerializer()

    class Meta:
        model = Lanes
        fields = [field.name for field in model._meta.fields if not field.primary_key]


class GameSerializer(NestedSerializer):
    player1 = PlayerSerializer()
    player2 = PlayerSerializer()
    player3 = PlayerSerializer()
    player4 = PlayerSerializer()
    lanes = LanesSerializer()
    deck = serializers.SerializerMethodField('game_deck')

    def game_deck(self, game):
        deck = Deck.objects.filter(game=game).values('card',).all()
        return deck

    class Meta:
        model = Game
        fields = '__all__'


class HandSerializer(NestedSerializer):
    card1 = CardSerializer()
    card2 = CardSerializer()
    card3 = CardSerializer()
    card4 = CardSerializer()
    card5 = CardSerializer()

    class Meta:
        model = Lane
        fields = [field.name for field in model._meta.fields if not field.primary_key]