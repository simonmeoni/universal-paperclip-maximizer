import logging
import re
import time

from dotenv import load_dotenv
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from aim import Run, Text

from chatbot import ChatBot, PROMPT
from environment import Environment
from tools import Tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()
MAX_TURNS = 200
MODEL = "gpt-4o"
CONTEXT_LENGTH = 5
PAUSE = 5

# Initialize Aim run
aim_run = Run()


def main(max_turns=MAX_TURNS):
    # Log hyperparameters
    aim_run["hparams"] = {"max_turns": max_turns, "model": MODEL, "prompt": PROMPT}

    # Initialize OpenAI client
    client = OpenAI()

    # initialize webdriver
    service = Service(executable_path="/opt/homebrew/bin/chromedriver")
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.decisionproblem.com/paperclips/index2.html")

    # Initialize chatbot and tools
    bot = ChatBot(PROMPT, client, MODEL, CONTEXT_LENGTH, logger)
    tools = Tools(driver, logger)
    environment = Environment(driver, logger)
    environment.driver.execute_script(
        """
                setInterval(function() {
                    document.getElementById('btnMakePaperclip').click();
                }, 100);
                """
    )
    game_state = environment.get_game_state()
    next_prompt = f"Observation: Game Started ! \n  Current Game State: {game_state}"
    aim_run.track(
        Text(next_prompt),
        name="game_state",
        step=0,
        context={"type": "state"},
    )
    aim_run.track(
        name="paperclips",
        value=int(re.search(r"Paperclips: (\d+)", game_state).group(1)),
        step=0,
        context={"type": "paperclips"},
    )
    i = 0
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        logger.info(result)
        aim_run.track(
            Text(result),
            name="bot_response",
            step=i - 1,
            context={"type": "response"},
        )

        # Execute actions
        extracted_re = tools.action_re.findall(result)

        result = "No actions were executed"
        if len(extracted_re) > 0:
            action, action_input = extracted_re[0]
            result = tools(action, action_input, environment)
        game_state = environment.get_game_state()
        next_prompt = (
            f"**Observation:**\n {result} \n\n **Current Game State:**\n\n {game_state}"
        )

        # Monitoring
        aim_run.track(
            name="paperclips",
            value=int(
                re.search(r"Paperclips: ([\d,]+)", game_state).group(1).replace(",", "")
            ),
            step=i,
            context={"type": "paperclips"},
        )
        aim_run.track(
            Text(next_prompt), name="game_state", step=i, context={"type": "state"}
        )
        logging.info(next_prompt)
        time.sleep(PAUSE)


if __name__ == "__main__":
    main()
