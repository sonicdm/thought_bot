# thought_bot
Thought bot: Kinda dumb therapy bot.
I made a bot that helped me put thoughts into perspective and turn them into a silly game concept instead of feeling overwhelmed.
uses the watson AI api from IBM

http://www.ibm.com/watson

## Usage
`python run.py`

### Choose your name
```
Welcome to the Thought Bot.
###########################

What is your name?: Player
```

### Answer a question
```
Thought #1 of 2
#####################################################
A random thought enters your head:
#####################################################
I will never be as good as {name}.


Its a Bad thought. How do you respond?
Choose an example that fits or type your own
#####################################################
#1: You will feel better if you ask.
#2: Don't take anything personally.
#3: These things happen sometimes.
#4: I dont need anyone else to have a good time.
#5: I am worth it.
Enter your response:2
```

### Check your answer
```
####################################################
You chose to think: Don't take anything personally.
That thought is a Good thought.
rated: {'Bad': 0, 'Good': 0, 'Neutral': 0.984352}
{u'tones': [{u'tone_name': u'Tentative', u'score': 0.984352, u'tone_id': u'tentative'}]}
Does this result work for you? [Y/n]: y
```
### End of round
```
Well done. You entered 2 thoughts. Lets see how you did.

The AI has judged your overall attitude as Good:
#####################################################
Tentative: 0.966403
Bad: 0
Good: 0
Neutral: 0.966403

Here are your thoughts for the round:
#####################################################

Good Thought: "Don't take anything personally."
\
 Thought Tones - Tentative: 0.984352
 Thought Alignment - Bad: 0 - Good: 0 - Neutral: 0.984352
Uncertain Thought: "I am going to go do that anyways."
\
 Thought Tones
 Thought Alignment - Bad: 0 - Good: 0 - Neutral: 0

All your thoughts individual scores combined came out to:
#####################################################
Bad: 0
Good: 0
Neutral: 0.966403
Press Enter To Continue
```


