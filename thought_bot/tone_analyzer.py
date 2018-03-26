"""
A thought experiment. Using python to train my brain into a healthy thought recognition process.
This will attempt to analyze a thought or concept into a rough calculation of what mood that thought likely represents.

Utilizes the IBM Watson AI's Tone Analyzer API
"""

from watson_developer_cloud.tone_analyzer_v3 import ToneAnalyzerV3
import random

# set tones and their thresholds for consideration
from thought_bot.config import bad_thoughts_path, good_thoughts_path

BAD_TONES = {
    'anger': .1,
    'sadness': .1,
    'fear': .1,
}

NEUTRAL_TONES = {
    'tentative': .1,
    'analytical': .1,
}

GOOD_TONES = {
    'joy': 0.1,
    'confident': .1,
}


def purge_from_dict_lists(obj, d):
    for k in d.iterkeys():
        if isinstance(d[k], list):
            while obj in d[k]:
                d[k].remove(obj)

class Brain(object):
    """
    This is your brain, there are many like it but this one is yours.
    """
    def __init__(self, name="Human"):
        self.name = name
        self._thoughts = {"All": [], "Good": [], "Bad": [], "Uncertain": []}
        self.banished_thoughts = 0

    def create_thought(self, thought_str, alignment=None):
        if isinstance(thought_str, (str,unicode)):
            thought = Thought(thought_str, self, alignment)
        else:
            thought = thought_str
        self._thoughts['All'].append(thought)
        self._thoughts[thought.alignment].append(thought)
        return thought

    def absorb_thoughts(self, l, alignment=None):
        while '' in l:
            l.remove('')
        for thought in l:
            self.create_thought(thought, alignment)

    def destroy_bad_thoughts(self):
        for thought in self._thoughts['Bad']:
            purge_from_dict_lists(thought, self._thoughts)

    def random_thoughts(self, alignment='All'):
        thoughts = [] + self._thoughts[alignment]
        random.shuffle(thoughts)
        return thoughts

    @property
    def random_thought(self):
        thoughts = [] + self._thoughts['All']
        random.shuffle(thoughts)
        return thoughts[0]

    @property
    def random_good_thoughts(self):
        # include neutral thoughts just in case.
        good_thoughts = [] + self._thoughts['Good'] + self._thoughts['Uncertain']
        random.shuffle(good_thoughts)
        yield good_thoughts
        
    def destroy_thought(self, thoughtobj):
        purge_from_dict_lists(thoughtobj, self._thoughts)
        self.banished_thoughts += 1

    def get_thought(self, alignment, idx=0):
        """

        :param alignment:
        :param idx:
        :return Thought
        :rtype Thought
        :returns Thought
        """
        thought = self._thoughts[alignment][idx]
        return thought

    def get_thoughts(self, alignment='All'):
        return self._thoughts[alignment]

    def __repr__(self):
        return "<{owner}'s Brain>".format(owner=self.name)


class Thought(object):
    """
    This is the byproduct of having a brain. You must decide what to do with it. Why cant AI help?
    """

    def __init__(self, thought, parent=None, alignment=None):
        self.bad_emotions = {}
        self.good_emotions = {}
        self.neutral_emotions = {}
        self.parent = parent
        if not self.parent:
            self.owner = 'Human'
        else:
            self.owner = getattr(self.parent, 'name')
        self.thought = thought
        self.thought_tone = None
        self.result = 'Uncertain'
        self.good_score = 0
        self.bad_score = 0
        self.neutral_score = 0
        self.tone_analyzer = ToneAnalyzerV3(version='2017-09-21',
                                            url='https://gateway.watsonplatform.net/tone-analyzer/api',
                                            username='0966265a-b0c0-4b35-9f8b-a53e934eeb1a',
                                            password='ukKiZ7JE2sbj'
                                            )
        if not alignment:
            self._alignment = self.decipher_thought(thought)
        else:
            self._alignment = {
                'Result': alignment,
                'Good': self.good_score,
                "Neutral": self.neutral_score,
                'Bad': self.bad_score
            }

    def decipher_thought(self, thought_str=None):
        if not thought_str:
            thought_str = self.thought
        if thought_str:
            self.thought_tone = self.tone_analyzer.tone(thought_str, content_type='text/plain')
            self.bad_emotions = self._toneload(BAD_TONES, self.thought_tone)
            self.good_emotions = self._toneload(GOOD_TONES, self.thought_tone)
            self.neutral_emotions = self._toneload(NEUTRAL_TONES, self.thought_tone)
            self.neutral_score = self.neutral_emotions['total_score']
            self.good_score = self.good_emotions['total_score']
            self.bad_score = self.bad_emotions['total_score']
            self.combined_score = self.neutral_score + self.good_score + self.bad_score

        # Figure out which emotion winds up weighing the most. Neutral emotions are weighted different for bad & good.
        if self.bad_score + (self.neutral_score * .7) > self.good_score + (self.neutral_score * .9):
            result = {'Result': 'Bad', 'Good': self.good_score,
                    "Neutral": self.neutral_score, 'Bad': self.bad_score}

        elif self.bad_score + (self.neutral_score * .7) < self.good_score + (self.neutral_score * .9):
            result = {'Result': 'Good', 'Good': self.good_score,
                      "Neutral": self.neutral_score, 'Bad': self.bad_score}

        elif self.neutral_score > self.bad_score and self.neutral_score > self.good_score or self.combined_score <= 0:
            result = {'Result': 'Uncertain', 'Good': self.good_score,
                    "Neutral": self.neutral_score, 'Bad': self.bad_score}
        self._alignment = result
        return result

    def _toneload(self, tone_dict, tone_response):
        emotion_dict = {'total_score': 0}
        for tone in tone_response['document_tone']['tones']:
            tone_id = tone.get('tone_id', None)
            tone_score = tone.get('score', None)
            if tone_id in tone_dict:
                if tone_score > tone_dict[tone_id]:
                    emotion_dict[tone_id] = tone_score
                    emotion_dict['total_score'] += tone_score

        return emotion_dict

    @property
    def scores(self):
        return {"Good": self.good_score, "Bad": self.bad_score, "Neutral": self.neutral_score}

    @property
    def alignment(self):
        return self._alignment['Result']

    @property
    def combined_score(self):
        return self.neutral_score + self.good_score + self.bad_score

    @combined_score.setter
    def combined_score(self, val):
        self._combined_score = val

    def __str__(self):
        return "<{owner}'s {alignment} Thought: {thought}>".format(
            owner=self.owner,
            alignment=self._alignment['Result'],
            thought=self.thought
        )

    def __unicode__(self):
        return u"<{owner}'s {alignment} Thought: {thought}>".format(
            owner=self.owner,
            alignment=self._alignment['Result'],
            thought=self.thought
        )


def load_thoughts():
    good_thoughts = []
    bad_thoughts = []
    with open(bad_thoughts_path) as f:
        for thought in f:
            bad_thoughts.append(thought.strip('\n'))

    with open(good_thoughts_path) as f:
        for thought in f:
            good_thoughts.append(thought.strip('\n'))
    return good_thoughts, bad_thoughts