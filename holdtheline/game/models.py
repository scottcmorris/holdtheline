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


class Lane(models.Model):
    TOP = 1
    MID = 0
    BOT = -1

    FLAG_LOCATION = (
        (BOT, 'Bottom'),
        (MID, 'Unclaimed'),
        (TOP, 'Top')
    )

    top1 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='top1')
    top2 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='top2')
    top3 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='top3')
    bot1 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='bot1')
    bot2 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='bot2')
    bot3 = models.ForeignKey(Card, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='bot3')
    flag = models.SmallIntegerField(choices=FLAG_LOCATION, default=0)

    def __str__(self):
        output = ''

        if self.flag == 1:
            output = 'X'
        if self.top1:
            output = '%s %s' % (output, self.top1)
        if self.top2:
            output = '%s %s' % (output, self.top2)
        if self.top3:
            output = '%s %s' % (output, self.top3)
        if self.flag == 0:
            output = '%s X' % output
        if self.bot1:
            output = '%s %s' % (output, self.bot1)
        if self.bot2:
            output = '%s %s' % (output, self.bot2)
        if self.bot3:
            output = '%s %s' % (output, self.bot3)
        if self.flag == -1:
            output = '%s X' % output

        return output

    def play_card(self, card, side):
        side = 'top' if str(side) == '1' or str(side) == 'top' else 'bot'
        if side == 'top':
            slot = self.find_open_slot(side)
            if slot == 1:
                self.top1 = card
            elif slot == 2:
                self.top2 = card
            elif slot == 3:
                self.top3 = card
            else:
                print('raise an error; no slot available')
                pass
        else:
            slot = self.find_open_slot(side)
            if slot == 1:
                self.bot1 = card
            elif slot == 2:
                self.bot2 = card
            elif slot == 3:
                self.bot3 = card
            else:
                print('raise an error; no slot available')

        return self


    def find_open_slot(self, side):
        if side == 'top':
            if self.top1 is None:
                return 1
            elif self.top2 is None:
                return 2
            elif self.top3 is None:
                return 3
            return -1
        else:
            if self.bot1 is None:
                return 1
            elif self.bot2 is None:
                return 2
            elif self.bot3 is None:
                return 3
            return -1


    def top_full(self):
        return bool(self.top1) + bool(self.top2) + bool(self.top3) == 3


    def bot_full(self):
        return bool(self.bot1) + bool(self.bot2) + bool(self.bot3) == 3


    def check_for_winner(self, side):
        if self.top_full() and self.get_value('top') > self.get_value('bot'):
            self.capture(self.TOP)
        elif self.bot_full() and self.get_value('bot') > self.get_value('top'):
            self.capture(self.BOT)
        return self


    def get_value(self, side):
        return self.get_value_top() if str(side) == '1' or str(side) == 'top' else self.get_value_bot()


    def get_value_top(self):
        value = 0
        if self.top1 is not None:
            value += self.top1
        if self.top2 is not None:
            value += self.top2
        if self.top3 is not None:
            value += self.top3
        return value


    def get_value_bot(self):
        value = 0
        if self.bot1 is not None:
            value += self.bot1
        if self.bot2 is not None:
            value += self.bot2
        if self.bot3 is not None:
            value += self.bot3
        return value


    def location(self):
        for loc in self.FLAG_LOCATION:
            if self.flag == loc[0]:
                return loc[1]
        return 'Unknown'


    def capture(self, location):
        if location != self.TOP and location != self.BOT:
            # raise error; can only capture top or bottom lane
            pass
        else:
            self.flag = location
            self.flag.save()


class Lanes(models.Model):
    lane1 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane1')
    lane2 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane2')
    lane3 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane3')
    lane4 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane4')
    lane5 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane5')
    lane6 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane6')
    lane7 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane7')
    lane8 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane8')
    lane9 = models.ForeignKey(Lane, null=False, blank=False, on_delete=models.CASCADE, related_name='lane9')

    def __str__(self):
        output = '%s %s %s %s %s %s %s %s %s' % (
            self.lane1.flag,
            self.lane2.flag,
            self.lane3.flag,
            self.lane4.flag,
            self.lane5.flag,
            self.lane6.flag,
            self.lane7.flag,
            self.lane8.flag,
            self.lane9.flag
        )
        return output


class Game(models.Model):
    player1 = models.ForeignKey(Player, null=False, related_name='player1',
                                on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, blank=True, null=True, related_name='player2',
                                default=None, on_delete=models.CASCADE)
    player3 = models.ForeignKey(Player, blank=True, null=True, related_name='player3',
                                default=None, on_delete=models.CASCADE)
    player4 = models.ForeignKey(Player, blank=True, null=True, related_name='player4',
                                default=None, on_delete=models.CASCADE)

    deck = models.ManyToManyField('Deck')

    lanes = models.ForeignKey(Lanes, null=False, on_delete=models.CASCADE)



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


class Deck(models.Model):
    game_fk = models.ForeignKey(Game, null=False, blank=False, default=-1,
                                on_delete=models.CASCADE, related_name='game_fk')
    card_fk = models.ForeignKey(Card, null=False, blank=False, default=-1,
                                on_delete=models.CASCADE, related_name='card_fk')
    player_fk = models.ForeignKey(Player, null=True, blank=True, default=None,
                                  on_delete=models.CASCADE)
    is_played = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return '%s %s %s %s' % (self.game_fk.pk, self.player_fk, self.card_fk, not(self.is_played))

    def play_card(self):
        self.is_played = True
        return self.card_fk

    def draw_card(self, player):
        self.player_fk = player
        return self.card_fk