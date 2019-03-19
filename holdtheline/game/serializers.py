from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from .models import Game, Card, Lane, Lanes, Deck, Player
from random import shuffle


class GameCreateSerializer(serializers.ModelSerializer):
    ## Serializer used to create games
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
            deck = Deck(game_fk=self.game, card_fk=card)
            deck.save()
            self.game.deck.add(deck)

class GameStartSerializer(serializers.ModelSerializer):
    ## Serializer used to Start games
    class Meta:
        model = Game
        fields = ('pk', 'turn')

    def update(self, game, validated_data):
        turn = validated_data.pop('turn')

        # If current turn is 0, then the game hasn't started.
        # If this serializer has a PUT for turn, then we can kick off a game
        if game.turn == 0 and turn > 0:
            # Need either 2 or 4 players to play
            players = game.player_count()
            if players % 2 == 0:
                game.next_turn()

                # Now let's deal some cards
                if players == 2:
                    hand_size = 7
                    player_list = [game.player1, game.player2]
                elif players == 4:
                    hand_size = 5
                    player_list = [game.player1, game.player2, game.player3, game.player4]

                for player in player_list:
                    for _ in range(0, hand_size * game.player_count()):
                        card = game.deck.objects.filter(game_fk=game, player_fk=None)[:1]
                        card.update(player_fk=player)
                        card.save()

                game.save()
        return game

    def retrieve(self, game, validated_data):
        return game


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




############### Basic Nested Serializers #################

class NestedSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop('nested', False)
        super().__init__(*args, **kwargs)
        if nested:
            self.fields.update(
                {'pk': serializers.IntegerField(validators=[])}
            )


class GameSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-games-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Game
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class LaneSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-lane-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Lane
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class CardSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-card-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Card
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class PlayerSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-player-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Player
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


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
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-lanes-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Lanes
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class DeckSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-deck-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Deck
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class WallhackGameSerializer(NestedSerializer):
    player1 = PlayerSerializer()
    player2 = PlayerSerializer()
    player3 = PlayerSerializer()
    player4 = PlayerSerializer()
    lanes = LanesSerializer()
    deck = DeckSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='wallhack-games-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Game
        fields = ['url'] + ['deck'] + [field.name for field in model._meta.fields if not field.primary_key]



########### Tabletop View: #############

class PlayerNoHandSerializer(NestedSerializer):

    class Meta:
        model = Player
        fields = ('nickname',)


class LanesReadOnlySerializer(NestedSerializer):
    lane1 = LaneSerializer(read_only=True)
    lane2 = LaneSerializer(read_only=True)
    lane3 = LaneSerializer(read_only=True)
    lane4 = LaneSerializer(read_only=True)
    lane5 = LaneSerializer(read_only=True)
    lane6 = LaneSerializer(read_only=True)
    lane7 = LaneSerializer(read_only=True)
    lane8 = LaneSerializer(read_only=True)
    lane9 = LaneSerializer(read_only=True)

    class Meta:
        model = Lanes
        fields = [field.name for field in model._meta.fields if not field.primary_key]


class TableSerializer(NestedSerializer):
    player1 = PlayerNoHandSerializer(read_only=True)
    player2 = PlayerNoHandSerializer(read_only=True)
    player3 = PlayerNoHandSerializer(read_only=True)
    player4 = PlayerNoHandSerializer(read_only=True)
    lanes = LanesReadOnlySerializer()

    class Meta:
        model = Game
        fields = '__all__'