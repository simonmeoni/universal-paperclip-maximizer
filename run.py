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
MAX_TURNS = 10
MODEL = "gpt-4o-mini"

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
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.decisionproblem.com/paperclips/index2.html")

    # Initialize chatbot and tools
    bot = ChatBot(PROMPT, client, MODEL, logger)
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

        extracted_re = tools.list_action_re.findall(result)
        action_results = "No actions were executed"
        if len(extracted_re) > 0:
            actions = extracted_re[0].split(",")
            if actions:
                for unparsed_action in actions:
                    if len(tools.action_re.findall(unparsed_action)) != 0:
                        action, action_input = tools.action_re.findall(unparsed_action)[
                            0
                        ]
                        tools(action_input)
                        time.sleep(0.5)
                        action_results = "The actions were successfully executed"
                    else:
                        logger.warning(
                            f"Action: {unparsed_action} is not a valid action"
                        )
                        action_results = (
                            f"The following action is not a valid action or "
                            f"malformed: {unparsed_action}"
                        )
        game_state = environment.get_game_state()
        next_prompt = (
            f"**Observation:**\n {action_results} \n\n **Current Game State:** "
            f"\n\n {game_state}"
        )
        aim_run.track(
            name="paperclips",
            value=int(re.search(r"Paperclips: (\d+)", game_state).group(1)),
            step=i,
            context={"type": "paperclips"},
        )
        aim_run.track(
            Text(next_prompt),
            name="game_state",
            step=i,
            context={"type": "state"},
        )
        logging.info(next_prompt)
        time.sleep(2)


if __name__ == "__main__":
    main()
