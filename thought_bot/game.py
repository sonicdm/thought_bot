import random
import re

import colorama

from thought_bot import an_or_a
from .config import default_round_length, default_round_count
from .tone_analyzer import Brain, Thought, load_thoughts


def clear_screen():
    print "\x1B[2J"


def start_game(player_name, host_name, alignment='Bad', num_rounds=default_round_count):
    # preload data
    colorama.init()
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
        self.host_thoughts = self.host_brain.random_thoughts(alignment)
        self.round_length = round_length
        self.round_score = 0
        self.round_alignment = {}

    def start(self):
        # ask the questions
        for i in xrange(1, self.round_length + 1):
            self._ask_question(i)

        # tally score
        self._end_of_round()

    def _end_of_round(self):
        clear_screen()
        player_thoughts = self.player_brain.get_thoughts()
        master_thought = self.player_brain.master_thought
        document_tone = master_thought.thought_tone['document_tone']
        sentences_tone = master_thought.thought_tone['sentences_tone']
        master_thought_score = master_thought.scores

        print "Well done. You entered {} thoughts. Lets see how you did.\n".format(len(player_thoughts))
        print "The AI has judged your overall attitude as {}:\n" \
              "#####################################################".format(master_thought.alignment['Result'])
        for tone in document_tone['tones']:
            trait = tone['tone_name']
            score = tone['score']
            print "{}: {}".format(trait, score)
        for attitude, score in master_thought.scores.iteritems():
            print "{}: {}".format(attitude, score)

        print colorama.Fore.LIGHTBLUE_EX
        print "Here are your thoughts for the round:\n" \
              "#####################################################"
        print colorama.Fore.WHITE
        for thought in player_thoughts:
            alignment = thought.alignment['Result']
            thought_tones_string = " Thought Tones"
            alignment_string = " Thought Alignment"
            print '{} Thought: "{}"\n' \
                  '\\'.format(alignment, thought.thought)
            for tone in thought.thought_tone['document_tone']['tones']:
                thought_tones_string += " - {}: {}".format(tone['tone_name'], tone['score'])
            print thought_tones_string
            for alignment, score in thought.scores.iteritems():
                alignment_string += " - {}: {}".format(alignment, score)
            print alignment_string

        print "\nAll your thoughts individual scores combined came out to:\n" \
              "#####################################################"
        for attitude, score in master_thought_score.iteritems():
            print "{}: {}".format(attitude, score)

        raw_input('Press Enter To Continue')

    def _ask_question(self, i):
        clear_screen()
        print "Thought #{} of {}".format(str(i), self.round_length)
        print "#####################################################\n" \
              "A random thought enters your head:\n" \
              "#####################################################"
        random.shuffle(self.host_thoughts)
        thought = self.host_thoughts.pop()
        good_thoughts = [] + self.good_thoughts
        random.shuffle(good_thoughts)
        while None in good_thoughts:
            good_thoughts.remove(None)
        alignment = thought.alignment['Result']
        print thought.thought
        print "\n\nIts {an} {alignment} thought. How do you respond?".format(an=an_or_a(alignment), alignment=alignment)
        print "Choose an example that fits or type your own\n" \
              "#####################################################"
        good_thought_choices = {k+1: v for k, v in enumerate(good_thoughts[:5])}
        for k, v in good_thought_choices.iteritems():
            print "#{k}: {v}".format(k=k, v=v.thought)
        player_input = None
        while not player_input:
            player_input = self._getresponse(good_thought_choices)
        self._respond(player_input)

    def _getresponse(self, thought_choices):
        player_input = raw_input('Enter your response:')
        response = None
        if player_input:
            try:
                selected = int(player_input)
                if 0 < selected <= len(thought_choices):
                    thought_response = thought_choices[selected]
                    response = thought_response
                else:
                    print "Invalid selection number selected"
                    response = None
            except ValueError:
                response = player_input
        return response

    def _respond(self, thought):
        if isinstance(thought, (str, bytes, unicode)):
            final_thought = Thought(thought, self.player_brain)
        else:
            final_thought = thought
            self.player_brain.create_thought(final_thought)
            if final_thought.combined_score <= 0:
                final_thought.decipher_thought()
        alignment = final_thought.alignment['Result']
        scores = final_thought.scores
        print "####################################################\n" \
              "You chose to think: {thought}".format(thought=final_thought.thought)
        print "That thought is {an} {alignment} thought.\nrated: {scores}".format(an=an_or_a(alignment),
                                                                                  alignment=alignment,
                                                                                  scores=scores)
        print final_thought.thought_tone['document_tone']
        confirm = raw_input('Does this result work for you? [Y/n]:')
        yes, no = False, False
        yesno = re.compile(r'((?P<yes>^(?:y|yes))$|^(?P<no>(?:n|yes)$))', re.I | re.M)
        yesnomatch = yesno.match(confirm)

        if yesnomatch:
            yes = yesno.match(confirm).group('yes')
            no = yesno.match(confirm).group('no')

        if yes or not confirm:
            self.round_score += 1

        if no:
            print "Go ahead and enter a new thought."
            self._getresponse(raw_input())

    def __str__(self):
        return "Thought Bot Game: Host: {host} Player: {player}".format(host=self.host_brain.name,
                                                                        player=self.player_brain.name)
