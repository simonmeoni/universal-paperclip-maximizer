import logging
import time

from dotenv import load_dotenv
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from chatbot import ChatBot, PROMPT
from environment import Environment
from tools import Tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()
MAX_TURNS = 30
MODEL = "gpt-4o-mini"



def main(max_turns=30):
    # Initialize OpenAI client
    client = OpenAI()

    # initialize webdriver
    service = Service(executable_path="/opt/homebrew/bin/chromedriver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.decisionproblem.com/paperclips/index2.html")



    # Initialize chatbot and tools
    bot = ChatBot(PROMPT, client, MODEL, logger)
    tools = Tools(driver, logger)
    environment = Environment(driver, logger)

    i = 0
    next_prompt = (
        f"Observation: Game Started ! \n  Current Game State: {environment.observation()} "
        f"\n Current Javascript Strategy: null"
    )
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        logger.info(result)
        actions = tools.action_re.findall(result)

        if actions:
            # There is an action to run
            action, action_input = actions[0]
            if action not in tools.known_actions.keys():
                logger.error(f"Unknown action: {action}: {action_input}")
                raise Exception(f"Unknown action: {action}: {action_input}")
            logger.info(f"Running {action} {action_input}")
            observations = tools.known_actions[action](action_input)
            logger.info(f"Observation: {observations}")
            next_prompt = (
                f"Observation: {observations} \n Current Game State: {environment.observation()}"
            )
        else:
            continue
        time.sleep(10)


if __name__ == "__main__":
    main()
