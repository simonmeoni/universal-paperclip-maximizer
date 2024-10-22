from openai import OpenAI

PROMPT = """
you are the best paperclip strategist maximize the number of paperclips you have by 
developing and executing JavaScript strategies that interact with the game.
You are playing the game of Paperclips, and your goal is to maximize the number of 
paperclips you have by developing and executing JavaScript strategies that interact with the game.

You run in a loop of Thought, Action, PAUSE, Observation, Current Game State and Current Javascript Strategy.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation, Current Game State and Current Javascript Strategy  will be the result of running those actions.

**The argument of each Action must be in this following format
such as 'Action: <action-name>: <javascript><action-argument></javascript>'**

Your available actions are:
- ModifyJavascriptStrategy: Modify a comprehensive JavaScript strategy that executes a series 
of actions (e.g., clicking buttons, buying upgrades) or monitors resources. This script in inside an 
interval function that runs every 200 milliseconds.

Start by observing the game state and then create a JavaScript strategy that aligns with your current goal. 
Modify the strategy if needed as the game progresses.

Example session:
you will be called with this first:
Observation: Game Started ! 
Current Game State: <html>
Current Strategy: null

Thought: I need to create a JavaScript strategy to maximize the number of paperclips.
Action: ModifyJavascriptStrategy: <javascript>
if (funds >= 5) { 
    document.getElementById('btnBuyClippers').click(); 
} 
document.getElementById('btnMakePaperclip').click();
</javascript>
PAUSE

You will be called again with this:
Observation: Strategy executed successfully
Current Game State: <html>
Current Strategy: <javascript> 
if (funds >= 5) { 
document.getElementById('btnBuyClippers').click(); 
} 
document.getElementById('btnMakePaperclip').click();
</javascript>

You then output:

Thought: I need to optimize my JavaScript strategy to maximize the number of paperclips.
Action: ModifyJavascriptStrategy: if (funds >= 5) { document.getElementById('btnBuyClippers').click(); } document.getElementById('btnMakePaperclip').click(); document.getElementById('btnBuyClippers').click(); document.getElementById('btnMakePaperclip').click();
PAUSE
""".strip()


class ChatBot:
    def __init__(self, system, client, model, logger):
        self.system = system
        self.messages = []
        self.client = client
        self.logger = logger
        self.model = model
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
            messages=self.messages[:1]
            + [message for message in self.messages if message["role"] == "assistant"]
            + self.messages[-1:],
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        self.logger.info(f"Token usage: {completion.usage}")
        return completion.choices[0].message.content
