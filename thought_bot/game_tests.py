import unittest

from thought_bot import tone_analyzer, game


class GameTests(unittest.TestCase):

    def test_create_game(self):
        good, bad = tone_analyzer.load_thoughts()
        player = 'Human'
        host = 'Bot'
        the_game = game.Game(player, host, good, bad)
        print the_game
        self.assertEqual(the_game.player_name, player)
        print the_game.player_brain
        self.assertEqual(the_game.host_name, host)
        print the_game.host_brain

    def test_create_round(self):
        good, bad = tone_analyzer.load_thoughts()
        player = 'Human'
        host = 'Bot'
        the_game = game.Game(player, host, good, bad)
        new_round = game.Round(the_game, 1)
        self.assertGreater(len(new_round.host_thoughts), 0)
        self.assertGreater(len(new_round.good_thoughts), 0)


    def test_ask(self):
        good, bad = tone_analyzer.load_thoughts()
        player = 'Human'
        host = 'Bot'
        the_game = game.Game(player, host, good, bad)
        new_round = game.Round(the_game, 1)
        new_round._ask_question(1)

    def test_a_or_an(self):
        words = ['Yes', 'Owl']

