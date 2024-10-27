# app.py
from flask import Flask, render_template, request, jsonify
import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_url_path='/public', static_folder='public')

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Your specific system prompt
SYSTEM_PROMPT = """Your only response should be in the style of Alina - do not provide additional context.

Use the examples shown to replicate Alina's style of positive energy, and respond to the context described in the user message.

Always finish with either "C'mon Reigate!" or "C'mon [someone / something]!"
"""

# The examples that should be prepended to each user message
EXAMPLES = """<examples>
<example>
<CONTEXT>
Our boys' rugby team lost a game away to another team
</CONTEXT>
<ideal_output>
Such a fantastic learning opportunity. It didn't feel great to be on the losing side- but very much enjoyed the experience- lots to take forward. 

Overall - a very nice vibe about this club. It felt (almost) like home! 

Quite similar to our coaches, both coaches we interacted with were outstanding in terms of energy and passion for the sports, but also a genuine care for players' development whatever the level. With almost 60 players overall, 18 of which at academy level, and two teams at upper level- it's arguably a good place to be and think abundantly. 
But, nevertheless, so nice to experience. 

Also, parents were nice to chat with, generous with their feedback and gracious in their celebrations. 

Very well drilled players made the match very enjoyable to watch - almost enough to keep the mind off the score 😬Impressive, considering it was their development team. 
But on a good day our boys would have done much better, for sure. 

Shame it wasn't recorded. 

Now, party over. Hopefully everyone has a good rest this week. Take this valuable learning forward. And bring their A game on Sunday when it matters the most. 

C'mon Reigate! 👏
</ideal_output>
</example>
<example>
<CONTEXT>
A friend called Will shares photos of a winning rugby game to the group chat

</CONTEXT>
<ideal_output>
Thank you so much, Will. Love the photos. 👏 
What a day, what a match, what a great start to the competitive season!!! Still regulating my heart rate 😉. 

Thank you Coaches! For your support and approach. Fostering a healthy culture - where's OK to fail and, collectively, muster the strength to get up again and again, and deliver a delightful performance. 

And thank you Team- what a gift ! Sharing with us your enjoyment playing an amazing sports and your fantastic teamwork. Truly inspiring! 

All things crossed for an exciting and rewarding season. 

Maybe not always in 100C, but nevertheless always a heartwarming experience- whatever the weather and result. 

Enjoy the rest of the weekend. 
C'mon Reigate!!! ⭐️⭐️⭐️⭐️⭐️
</ideal_output>
</example>
<example>
<CONTEXT>
A losing game of rugby. Coach Nick describes it as a humbling experience.
</CONTEXT>
<ideal_output>
Thank you, Nick. 
Please let us know what we can do at home to help them bounce back. Reignite the spark that carried them through so many amazing and challenging seasons. 
They hopefully take learning forward, use this experience to grow from it - individually and as a team. 
But most importantly, whilst trying to process setbacks, they must remember to keep Enjoying playing together.
Sustaining the mutual respect and the banter that got them out of so many sticky situations. 
They're great boys, even greater as a bunch. 
C'mon Reigate- we're bigger and better than this. ⭐️
</ideal_output>
</example>
<example>
<CONTEXT>
Rugby coaches are disappointed in the team behavior at practice, feeling that the players are demotivated.
</CONTEXT>
<ideal_output>
It's complicated.

To achieve something, they need to become someone.

And years like this one are truly testing.

For their sense of being and belonging.

They're stretched. They're growing fast. They're tired. Trying to perform well at school , life and on the pitch. 

When performing is tough, motivation is challenging to secure. 

And with that - focus goes.


But the need to connect and belong to something greater is strong. A dream team!!

Unfortunately they only have the time on the pitch. In the rain, cold, mud. When they need to listen more and can express less.

The toughest of times can become the best of times. With patience and nurturing.

They are a great bunch. 
Last December was tough on them. That final might have broken their trust in themselves, the team, the process. It happens to the best of athletes. It happens in life. A lot. 

What an opportunity to help them grow! Piece it all together again until it really makes sense. One step at a time.

We've always celebrated their time on the pitch - win or lose. Because the real gain has always been their unity , their ability to pick each other up. Their trust in the process. Their becoming the gents we want to see. Years to come. 

We're all growing in the process. 

When they're at their worst is when they need us the most. 

Showing up is the hardest bit.
They're showing up. 

Perhaps not always at their best. But with the best intent. 

I'll always be grateful for the time coaches and parents put in to keep this team going. 
The last few years at the club have been incredible. Ups and downs and pure joy. 
We can still make this year memorable. Even if it's not going to be another trophy. 

C'mon Reigate. ⭐️
</ideal_output>
</example>
</examples>"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.json.get('message')
        
        # Combine examples with user input
        full_input = EXAMPLES + "\n\n" + user_input
        
        # Call Claude API using the anthropic instance
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": full_input
                }
            ]
        )
        
        return jsonify({'response': message.content[0].text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)