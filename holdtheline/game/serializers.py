from rest_framework import serializers
from .models import Game, Card, CardLocation, Player, Flag
from random import shuffle

class GameCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('pk', 'player1',)

    def create(self, validated_data):
        self.create_game(validated_data)
        self.setup_flags()
        self.shuffle_deck()

        return self.game

    def create_game(self, validated_data):
        player1 = validated_data.pop('player1')
        if isinstance(player1, Player):
            self.game = Game(player1=player1)
            self.game.save()

    def setup_flags(self):
        for i in range(1, 10):
            flag = Flag(game=self.game, lane=i)
            flag.save()

    def shuffle_deck(self):
        cards = list(Card.objects.all())
        shuffle(cards)

        for card in cards:
            card_loc = CardLocation(game=self.game, card=card)
            card_loc.save()



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