import time

from openai import OpenAI

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
service = Service(executable_path="/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.decisionproblem.com/paperclips/index2.html")

prompt = """
you are the best paperclip strategist maximize the number of paperclips you have by 
developing and executing JavaScript strategies that interact with the game.
You are playing the game of Paperclips, and your goal is to maximize the number of 
paperclips you have by developing and executing JavaScript strategies that interact with the game.

You run in a loop of Thought, Action, PAUSE, Observation, Current Game State and Current Javascript Strategy.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation, Current Game State and Current Javascript Strategy  will be the result of running those actions.

**The argument of each Action must be in the same line as the action name and only in one line.
such as 'Action: <action-name>: <action-argument>'**

Your available actions are:
- ModifyJavascriptStrategy: Modify a comprehensive JavaScript strategy that executes a series 
of actions (e.g., clicking buttons, buying upgrades) or monitors resources.

Start by observing the game state and then create a JavaScript strategy that aligns with your current goal. 
Modify the strategy if needed as the game progresses.

Example session:
you will be called with this first:
Observation: Game Started ! 
Current Game State: <html>
Current Strategy: null

Thought: I need to create a JavaScript strategy to maximize the number of paperclips.
Action: ModifyJavascriptStrategy: if (funds >= 5) { document.getElementById('btnBuyClippers').click(); } document.getElementById('btnMakePaperclip').click();
PAUSE

You will be called again with this:
Observation: Strategy executed successfully
Current Game State: <html>
Current Strategy: if (funds >= 5) { document.getElementById('btnBuyClippers').click(); } document.getElementById('btnMakePaperclip').click();

You then output:

Thought: I need to optimize my JavaScript strategy to maximize the number of paperclips.
Action: ModifyJavascriptStrategy: if (funds >= 5) { document.getElementById('btnBuyClippers').click(); } document.getElementById('btnMakePaperclip').click(); document.getElementById('btnBuyClippers').click(); document.getElementById('btnMakePaperclip').click();
PAUSE
""".strip()


class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=self.messages[:1] + self.messages[-2:],
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        print(completion.usage)
        return completion.choices[0].message.content


def main(max_turns=30):
    # Set up ChromeDriver
    action_re = re.compile("^Action: (\w+): (.*)$")

    i = 0
    bot = ChatBot(system=prompt)
    next_prompt = f"Observation: Game Started ! \n  Current Game State: {observation()} \n Current Javascript Strategy: null"
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions.keys():
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observations = known_actions[action](action_input)
            print("Observation:", observations)
            next_prompt = f"Observation: {observations} \n Current Game State: {observation()}"
        else:
            continue
        time.sleep(10)


def observation():
    """
    Observes the current state of the game by fetching the entire HTML of the page.
    Returns the HTML as a string.
    """
    try:
        html_content = driver.page_source.replace("\n", "")
        return html_content
    except Exception as e:
        print(f"Error during observation: {e}")
        return None


def modify_javascript_strategy(strategy_script):
    """
    Modifies the JavaScript strategy by replacing the old one if it exists.
    Returns the result of the operation.
    """
    try:
        # JavaScript to check if a strategy already exists and clear it if needed
        driver.execute_script(
            """
            // Check if a previous strategy exists and clear the interval
            if (window.activeStrategyInterval) {
                clearInterval(window.activeStrategyInterval);
                console.log('Previous strategy cleared');
            }

            // Set the new strategy with setInterval and store it globally
            window.activeStrategyInterval = setInterval(() => { %s }, 2000);
            console.log('New strategy set');
            """ % strategy_script
        )
        return "Strategy replaced successfully"
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return None


known_actions = {
    "ModifyJavascriptStrategy": modify_javascript_strategy,
}

if __name__ == "__main__":
    main()
