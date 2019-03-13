from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Player, Game, Flag, Card, CardLocation
from users.models import User

class GamesModelTestCase(TestCase):

    def setUp(self):
        pass


    def create_users(self, count):
        """Create a list of User instances for testing."""

        users = []

        for i in range(1, count+1):
            user = User(f'user{i}', '', 'password')
            user.save()
            users.append(user)

        return users

    def create_players(self, users):
        """Create a list of Player instances from a list of User
           instances for testing."""

        players = []

        for i, user in enumerate(users):
            player = Player(user=user, nickname=f'Swindle_{i}')
            player.save()
            players.append(player)

        return players

    def create_game(self, player_count, turn=0):
        """Create a Game instance for testing."""

        users = self.create_users(player_count)
        players = self.create_players(users)

        # Fill up the list with Nones to instantiate Game() if player_count < 4
        if player_count < 4:
            players.append(*([None] * (4 - player_count)))

        game = Game(player1=players[0],
                    player2=players[1],
                    player3=players[2],
                    player4=players[3])
        game.save()
        return game

    def test_game_creation(self):
        """Test that Game instances are instantiated correctly."""

        game = Game(players=4, turn=0)

        self.assertTrue(isinstance(game, Game))
        self.assertEqual(str(game), 'The game is not currently active.')
        self.assertEqual(game.player_count(), 4)

        game = Game(players=2, turn=2)
        self.assertTrue(isinstance(game, Game))
        self.assertEqual(str(game), 'It is Swindle_2\'s turn.')
        self.assertEqual(game.player_count(), 2)


    def create_flag(self, game, lane=1, won=0):
        """Create a Flag instance for testing."""
        flag = Flag(game=game, lane=lane, won=won)
        flag.save()

        return flag

    def create_flags(self, game, count=9):
        """Create a list of Flag instances for testing."""
        flags = []
        for lane in range(1, count+1):
            flag = create_flag(game=game, lane=lane)
            flags.append(flag)

        return flags

    def test_flag_creation(self):
        """Test that Flag instances are created correctly."""
        game = self.create_game()
        flag = create_flag(game=game, lane=1)

        self.assertTrue(isinstance(flag, Flag))
        self.assertEqual(str(flag), 'Lane 1: Middle')

    def test_flag_capture(self):
        """Test that flags can be captured correctly."""

        game = self.create_game()
        flag = self.create_flag(game=game, lane=1)

        flag.capture(flag.BOT)
        self.assertEqual(str(flag), 'Lane 1: Bottom')
        self.assertRaises(flag.capture(flag.MID))

)
