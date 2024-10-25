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
MAX_TURNS = 100
MODEL = "gpt-4o"


def main(max_turns=MAX_TURNS):
    # Initialize OpenAI client
    client = OpenAI()

    # initialize webdriver
    service = Service(executable_path="/opt/homebrew/bin/chromedriver")
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)
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
    i = 0
    next_prompt = f"Observation: Game Started ! \n  Current Game State: {environment.observation()} "
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        logger.info(result)
        extracted_re = tools.list_action_re.findall(result)
        if len(extracted_re) == 0:
            continue
        else:
            actions = extracted_re[0].split(",")
            observations = ""
            if actions:
                for unparsed_action in actions:
                    if len(tools.action_re.findall(unparsed_action)) != 0:
                        action, action_input = tools.action_re.findall(unparsed_action)[
                            0
                        ]
                        tools(action_input)
                        time.sleep(0.5)
                        observations = "The actions were successfully executed"

                    else:
                        logger.warning(
                            f"Action: {unparsed_action} is not a valid action"
                        )
                        observations = f"The following action is not a valid action or malformed: {unparsed_action}"
            else:
                continue
        next_prompt = (
            f"**Observation:**\n {observations} \n\n **Current Game State:** "
            f"\n\n {environment.observation()}"
        )
        logging.info(next_prompt)
        time.sleep(2)


if __name__ == "__main__":
    main()
