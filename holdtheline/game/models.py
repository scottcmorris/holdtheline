import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token
from holdtheline.users.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15)

    def __str__(self):
        if self.nickname:
            return u'%s' % (self.nickname)
        else:
            return u'%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ("user",)


class Game(models.Model):
    player1 = models.ForeignKey(Player, null=False, related_name='player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, blank=True, null=True, related_name='player2',
                                default=None, on_delete=models.CASCADE)
    player3 = models.ForeignKey(Player, blank=True, null=True, related_name='player3',
                                default=None, on_delete=models.CASCADE)
    player4 = models.ForeignKey(Player, blank=True, null=True, related_name='player4',
                                default=None, on_delete=models.CASCADE)

    player_list = [
        None,
        player1,
        player2,
        player3,
        player4,
    ]

    turn = models.PositiveSmallIntegerField(default=0, validators=[
            MaxValueValidator(4),
            MinValueValidator(0)
        ])

    def __str__(self):
        return u'Game %s; Players: %s; Status: %s' % (self.pk, self.player_names(), self.current_player())

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

    def set_player(self, number, player):
        if number == 1:
            self.player1 = player
        elif number == 2:
            self.player2 = player
        elif number == 3:
            self.player3 = player
        elif number == 4:
            self.player4 = player
        self.save()

    def swap_players(self, i, j):
        self.players[i], self.players[j] = self.players[j], self.players[i]
        self.save()

    def player_count(self):
        return bool(self.player1) + bool(self.player2) + bool(self.player3) + bool(self.player4)

    def player_names(self):
        result = self.player1
        if self.player2:
            result = '%s, %s' % (result, self.player2)
        if self.player3:
            result = '%s, %s' % (result, self.player3)
        if self.player4:
            result = '%s, %s' % (result, self.player4)
        return result

    def current_player(self):
        if self.turn == 0:
            result = 'Inactive'
        else:
            if self.turn == 1:
                result = self.player1
            elif self.turn == 2:
                result = self.player2
            elif self.turn == 3:
                result = self.player3
            elif self.turn == 4:
                result = self.player4
            result = '%s\'s turn.' % result
        return result

    def next_turn(self):
        if self.turn < self.player_count():
            self.turn += 1
        else:
            self.turn = 1
        self.save()

    def get_player_by_value(self, value):
        if value == 1:
            results = self.player1
        elif value == 2:
            results = self.player2
        elif value == 3:
            results = self.player3
        elif value == 4:
            results = self.player4
        return results




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

    def __str__(self):
        return u'Game: %s; Lane %s: %s' % (self.game.pk, self.lane, self.location())

    def location(self):
        for loc in self.FLAG_LOCATION:
            if self.won == loc[0]:
                return loc[1]
        return 'Unknown'

    def capture(self, location):
        if location != self.TOP and location != self.BOT:
           # raise error; can only capture top or bottom lane
           pass
        else:
            self.won = location
            self.won.save()

    class Meta:
        ordering = ("-game", "lane",)



class Card(models.Model):
    GREEN = 0
    RED = 1
    ORANGE = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5

    SHORT_NAME = ('G', 'R', 'O', 'B', 'Y', 'P')

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

    def __str__(self):
        return u'%s%s' % (self.SHORT_NAME[self.color], self.value)

    class Meta:
        ordering = ("color", "value")
        unique_together = (("color", "value"),)


def location_map():
    deck = 0
    hand = [1, 2, 3, 4]
    lane = [x for x in range(5, 59)]

    locations = (
        (deck, 'Deck'),
        *tuple((x, 'Player %s' % x) for x in hand),
        *tuple((x, get_lane_details(x)) for x in lane)
    )

    return locations

def get_lane_details(value):
    value += 1

    lane = value // 6
    side = 'Top' if (value // 3) % 2 else 'Bottom'
    slot = (value % 3) + 1

    return u'Lane: %s; Side: %s; Slot: %s' % (lane, side, slot)


class CardLocation(models.Model):

    locations = location_map()

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    location = models.SmallIntegerField(choices=locations, default=0)

    class Meta:
        ordering = ("-game", "location",)

    def __str__(self):
        return u'Game: %s; Card: %s; Location: %s' % (self.game.pk, self.card, self.get_location_type())

    def get_location_type(self):
        if self.location == 0:
            return 'Deck'
        elif self.location < 5:
            return self.game.get_player_by_value(self.location)
        else:
            return get_lane_details(self.location)







