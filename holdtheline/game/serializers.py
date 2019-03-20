from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from .models import Game, Card, Lane, Lanes, Deck, Player
from random import shuffle


############ Helper classes, functions, serializers ###########
class NestedSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop('nested', False)
        super().__init__(*args, **kwargs)
        if nested:
            self.fields.update(
                {'pk': serializers.IntegerField(validators=[])}
            )


############# Administrative serializers #################
## Game
##
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

                # Now let's deal some cards
                if players == 2:
                    hand_size = 7
                    player_list = [game.player1, game.player2]
                elif players == 4:
                    hand_size = 5
                    player_list = [game.player1, game.player2, game.player3, game.player4]

                for player in player_list:
                    for _ in range(0, hand_size):
                        card = Deck.objects.filter(game_fk=game, player_fk=None)[0]
                        card.player_fk = player
                        card.save()

                game.next_turn()
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


class GameSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='game-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Game
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]

## Player
##
class PlayerSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='player-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Player
        fields = ['url'] + [field.name for field in model._meta.fields if not field.primary_key]


class GamePlayerSerializer(PlayerSerializer):

    class Meta:
        model = Player
        fields = '__all__'

## Lanes
##

class LaneSerializer(NestedSerializer):

    class Meta:
        model = Lane
        fields = [field.name for field in model._meta.fields if not field.primary_key]

class GameLanesLaneSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='lane-detail',
    )

    class Meta:
        model = Lane
        fields = '__all__'


class GameLanesSerializer(NestedSerializer):
    lane1 = GameLanesLaneSerializer()
    lane2 = GameLanesLaneSerializer()
    lane3 = GameLanesLaneSerializer()
    lane4 = GameLanesLaneSerializer()
    lane5 = GameLanesLaneSerializer()
    lane6 = GameLanesLaneSerializer()
    lane7 = GameLanesLaneSerializer()
    lane8 = GameLanesLaneSerializer()
    lane9 = GameLanesLaneSerializer()

    url = serializers.HyperlinkedIdentityField(
        view_name='game-lanes-list',
        lookup_field='pk'
    )

    class Meta:
        model = Lanes
        fields = '__all__'

## Deck
##


class DeckSerializer(NestedSerializer):

    class Meta:
        model = Deck
        fields = [field.name for field in model._meta.fields if not field.primary_key]


class GameDeckCardSerializer(NestedSerializer):

    class Meta:
        model = Deck
        fields = '__all__'


class GameDeckSerializer(NestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='deck-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Deck
        fields = '__all__'

## Card
##

class CardSerializer(NestedSerializer):

    class Meta:
        model = Card
        fields = '__all__'


## Consolidated View
##

class GameFullSerializer(NestedSerializer):
    player1 = PlayerSerializer()
    player2 = PlayerSerializer()
    player3 = PlayerSerializer()
    player4 = PlayerSerializer()
    lanes = GameLanesSerializer()
    deck = GameDeckSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='game-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Game
        fields = ['url'] + ['deck'] + [field.name for field in model._meta.fields if not field.primary_key]


########### Player Serializers: #############

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