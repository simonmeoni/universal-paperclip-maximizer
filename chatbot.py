PROMPT = """
you are the best paperclip strategist maximize the number of paperclips you have by 
developing and executing JavaScript strategies that interact with the game.
You are playing the game of Paperclips, and your goal is to maximize the number of 
paperclips you have by interacting with the game using the provided actions.

You run in a loop of Thought, a list of Action, PAUSE, Observation, Current Game State.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use a Available Actions to run one of the action n between 1 and 20 times available to you - then return PAUSE.
Observation, Current Game State will be the result of running those actions.

The list of available actions will be return by the game state section in this format:

Action Available: 
Make Paperclip
lower
raise
Marketing
Wire

**The argument of each Action must be in this following format such as 'Action: <action-name>: <action-argument>'**

Start by observing the game state and then create a strategy that aligns with your goal. 
Modify the strategy if needed as the game progresses.

Example session:
you will be called with this first:

**Observation:** 
Game Started ! 

**Current Game State:** 
Paperclips: 35
Make Paperclip
Business
Available Funds: $ 1.00
Unsold Inventory: 31
lower raise Price per Clip: $ .25
Public Demand: 32%
Marketing Level: 1
Cost: $ 100.00
Manufacturing
Clips per Second: 10
Wire 965 inches
Cost: $ 20 

**Action Available:** 
Make Paperclip
lower
raise
Marketing
Wire

Thought: I need to buy AutoClipper to maximize the number of paperclips.
Action: lower: 5
PAUSE

You will be called again with this:

**Observation:** 
Action were successfully executed

**Current Game State:** 
Paperclips: 35
Make Paperclip
Business
Available Funds: $ 1.00
Unsold Inventory: 31
lower raise Price per Clip: $ .25
Public Demand: 32%
Marketing Level: 1
Cost: $ 100.00
Manufacturing
Clips per Second: 10
Wire 965 inches
Cost: $ 20 

**Action Available:** 
Make Paperclip
lower
raise
Marketing
Wire


You then output:
Thought: I need to reduce the cost of paperclips to increase profits.
Action: Marketing: 1
PAUSE
""".strip()


class ChatBot:
    def __init__(self, system, client, model, context_length ,logger):
        self.system = system
        self.messages = []
        self.client = client
        self.logger = logger
        self.model = model
        self.context_length = context_length
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages[:1] + self.messages[1:][-self.context_length:]
        )
        self.logger.info(f"Token usage: {completion.usage}")
        return completion.choices[0].message.content
