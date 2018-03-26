from thought_bot import an_or_a
from .tone_analyzer import Brain, Thought, load_thoughts
from .config import default_round_length, default_round_count
import random


def start_game(player_name, host_name, alignment='Bad', num_rounds=default_round_count):
    # preload data
    good, bad = load_thoughts()
    host_brain = Brain(host_name)
    host_brain.absorb_thoughts(good, "Good")
    host_brain.absorb_thoughts(bad, "Bad")
    game = Game(player_name, host_name, good, bad)
    game.start(default_round_length,alignment,num_rounds)


class Game(object):

    def __init__(self, player, host, good, bad, round_count=default_round_count):
        self.round_number = 0
        self.player_name = player
        self.host_name = host
        self.good_list = good
        self.bad_list = bad
        self.host_brain = Brain(host)
        self.player_brain = Brain(player)
        self.host_brain.absorb_thoughts(self.good_list, "Good")
        self.host_brain.absorb_thoughts(self.bad_list, "Bad")

    def start(self, round_length=default_round_length, alignment='Bad', num_rounds=1):
        for i in xrange(1, num_rounds+1):
            print "Starting Round #{}".format(i)
            round = Round(self, round_length, alignment)
            round.start()



class Round(object):
    def __init__(self, parent, round_length, alignment="Bad"):
        self.host_brain = getattr(parent, 'host_brain')
        self.player_brain = getattr(parent, "player_brain")
        self.good_thoughts = self.host_brain.random_thoughts('Good')
        self.thoughts = self.host_brain.random_thoughts(alignment)
        self.round_length = round_length

    def start(self):
        for i in xrange(1, self.round_length):
            self._ask_question(i)

    def _end_of_round(self):

        pass

    def _ask_question(self, i):
        print "Thought #" + str(i)
        print "##################################\n" \
              "A random thought enters your head:\n" \
              "##################################"
        random.shuffle(self.thoughts)
        thought = self.thoughts.pop()
        good_thoughts = [] + self.good_thoughts
        random.shuffle(good_thoughts)
        while None in good_thoughts:
            good_thoughts.remove(None)
        alignment = thought.alignment
        print thought.thought
        print "\n\nIts {an} {alignment} thought. How do you respond?".format(an=an_or_a(alignment), alignment=alignment)
        print "Choose an example that fits or type your own\n" \
              "##################################"
        good_thought_choices = {k+1: v for k, v in enumerate(good_thoughts[:5])}
        for k, v in good_thought_choices.iteritems():
            print "#{k}: {v}".format(k=k, v=v.thought)
        player_input = raw_input('Enter your response:')
        try:
            selected = int(player_input)
            thought_response = good_thought_choices[selected]
            self._respond(thought_response)
        except ValueError:
            self._respond(player_input)

    def _respond(self, thought):
        if isinstance(thought, (str, bytes, unicode)):
            final_thought = Thought(thought, self.player_brain)
        else:
            final_thought = thought
            final_thought.parent = self.player_brain
            if final_thought.combined_score <= 0:
                final_thought.decipher_thought()
        alignment = final_thought.alignment
        scores = final_thought.scores
        print "###################################\n" \
              "You chose to think: {thought}".format(thought=final_thought.thought)
        print "That thought is {an} {alignment} thought.\nrated: {scores}".format(an=an_or_a(alignment),
                                                                                  alignment=alignment,
                                                                                  scores=scores)
        print  final_thought.thought_tone['document_tone']
        confirm = raw_input('Enter to continue')

    def __str__(self):
        return "Thought Bot Game: Host: {host} Player: {player}".format(host=self.host_brain.name,
                                                                        player=self.player_brain.name)
