import unittest

import thought_bot.tone_analyzer
from thought_bot import tone_analyzer, game, config




class BrainTests(unittest.TestCase):

    def test_brain_create(self):
        brain = tone_analyzer.Brain('Name')
        self.assertEqual(brain.name, 'Name')

    def test_create_thought(self):
        brain = tone_analyzer.Brain()

        bad_thought = tone_analyzer.Thought("This thought is completely stupid and dumb", brain)
        uncertain_thought = tone_analyzer.Thought("I cant wait for this party, it's going to be so fun!", brain)
        good_thought = tone_analyzer.Thought("I am excited about this amazing new project.", brain)

        print bad_thought
        self.assertEqual(bad_thought.thought, "This thought is completely stupid and dumb")
        print uncertain_thought
        self.assertEqual(uncertain_thought.thought, "I cant wait for this party, it's going to be so fun!")
        print good_thought
        self.assertEqual(good_thought.thought, "I am excited about this amazing new project.")

    def test_decipher_thought(self):
        brain = tone_analyzer.Brain('Name')
        bad_thought = "This thought is completely stupid and dumb."
        good_thought = "I am happy about this sentence."
        uncertain_thought = "I cant wait for this party, it's going to be so fun!"
        brain.create_thought(bad_thought)
        brain.create_thought(good_thought)
        brain.create_thought(uncertain_thought)
        bad_result = brain.get_thought('Bad', 0)
        print bad_result
        print bad_result.thought
        self.assertEqual(bad_result.thought, bad_thought)
        self.assertEqual(bad_result.alignment, 'Bad')
        good_result = brain.get_thought('Good', 0)
        print good_result
        print good_result.thought
        self.assertEqual(good_result.thought, good_thought)
        self.assertEqual(good_result.alignment, 'Good')
        uncertain_result = brain.get_thought('Uncertain', 0)
        print uncertain_result
        print uncertain_result.thought
        self.assertEqual(uncertain_result.thought, uncertain_thought)
        self.assertEqual(uncertain_result.alignment, 'Uncertain')

    def test_load_thoughts(self):
        good, bad = tone_analyzer.load_thoughts()
        self.assertIn('I am worth it.', good)
        self.assertIn('I am unlovable.', bad)

    def test_absorb_thoughts(self):
        brain = tone_analyzer.Brain('Name')
        thought_list = tone_analyzer.load_thoughts()[0]
        brain.absorb_thoughts(thought_list, 'Good')
        thought_result = brain.get_thoughts()

        for t in thought_result:
            self.assertIn(t.thought, thought_list)




