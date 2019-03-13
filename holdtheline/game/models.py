import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token


class Player(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15)

    def __unicode__(self):
        if self.nickname:
            return u'%s' % (self.nickname)
        else:
            return u'%s' % (self.user.first_name)


class Game(models.Model):
    player1 = models.ForeignKey('Player', null=False, related_name='player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey('Player', null=True, related_name='player2',
                                default=None, on_delete=models.CASCADE)
    player3 = models.ForeignKey('Player', null=True, related_name='player3',
                                default=None, on_delete=models.CASCADE)
    player4 = models.ForeignKey('Player', null=True, related_name='player4',
                                default=None, on_delete=models.CASCADE)

    player_list = [
        None,
        player1,
        player2,
        player3,
        player4,
    ]

    turn = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(4),
            MinValueValidator(0)
        ])

    def __unicode__(self):
        if self.turn == 0:
            return u'The game is not currently active.'
        else:
            return u'It is %s\'s turn.' % player_list[turn]

    def add_player(self, player):
        if self.player_count() > 4:
            # no more spots
            pass
        elif self.player_count() == 1:
            self.player2 = player
        elif self.player_count() == 2:
            self.player3 = player
        else:
            self.player4 = player

        self.save()

    def swap_players(self, i, j):
        self.players[i], self.players[j] = self.players[j], self.players[i]

        self.save()

    def player_count(self):
        return bool(player1) + bool(player2) + bool(player3) + bool(player4)

    def next_turn(self):
        if self.turn < self.player_count():
            self.turn += 1
        else:
            self.turn = 1
        self.save()


class Flag(models.Model):
    TOP = 1
    MID = 0
    BOT = -1

    FLAG_LOCATION = (
        (BOT, 'Bottom'),
        (MID, 'Unclaimed'),
        (TOP, 'Top')
    )

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    lane = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(9),
            MinValueValidator(1)
        ])
    won = models.SmallIntegerField(choices=FLAG_LOCATION, default=0)

    def __unicode__(self):
        return u'Lane %s: %s' % (self.lane, self.won)

    def capture(self, location):
        if location != self.TOP and location != self.BOT:
           # raise error; can only capture top or bottom lane
           pass
        else:
            self.won = location
            self.won.save()


class Card(models.Model):
    GREEN = 0
    RED = 1
    ORANGE = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5

    COLORS = (
        (GREEN, 'Green'),
        (RED, 'Red'),
        (ORANGE, 'Orange'),
        (BLUE, 'Blue'),
        (YELLOW, 'Yellow'),
        (PURPLE, 'Purple')
    )

    color = models.PositiveSmallIntegerField(choices=COLORS)
    value = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])

    def __unicode__(self):
        return u'%s (%s)' % (self.color, self.value)


def get_lane_details(value):
    value += 1

    lane = value // 6
    side = 'Top' if (value // 3) % 2 else 'Bottom'
    slot = (value % 3) + 1

    return u'Lane: %s, Side: %s, Slot: %s' % (lane, side, slot)

class CardLocation(models.Model):
    DECK = 0
    HAND = [1, 2, 3, 4]
    LANE = [x for x in range(5, 59)]

    LOCATIONS = (
        (DECK, 'Deck'),
        *tuple((x, 'Player %s' % x) for x in HAND),
        *tuple((x, get_lane_details(x)) for x in LANE)
    )

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    location = models.SmallIntegerField(choices=LOCATIONS)

    def __unicode__(self):
        return u'Game: %s, Card: %s, Location: %s' % (self.game, self.card, self.location)
