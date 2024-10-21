import time
import logging
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
from dotenv import load_dotenv
from unstructured.partition.html import partition_html

from selenium.webdriver import ChromeOptions
opts = ChromeOptions()
opts.add_experimental_option("detach", True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI()
service = Service(executable_path="/opt/homebrew/bin/chromedriver")

# Add these options to keep the browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.decisionproblem.com/paperclips/index2.html")

prompt = """
you are the best paperclip strategist maximize the number of paperclips you have by 
developing and executing JavaScript strategies that interact with the game.
you are making paperclips out of WIRE, you need one WIRE to make a single paperclip
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
of actions (e.g., clicking buttons, buying upgrades) or monitors resources.

Here is the list of actions you can take and use in the Javascript code you create:
{
  "actions": [
    {
      "name": "Make Paperclip",
      "elementId": "btnMakePaperclip",
      "elementType": "button",
      "onclickFunction": "makePaperclip()",
      "category": "Manufacturing"
    },
    {
      "name": "Lower Price",
      "elementId": "btnLowerPrice",
      "elementType": "button",
      "onclickFunction": "lowerPrice()",
      "category": "Business"
    },
    {
      "name": "Raise Price",
      "elementId": "btnRaisePrice",
      "elementType": "button",
      "onclickFunction": "raisePrice()",
      "category": "Business"
    },
    {
      "name": "Upgrade Marketing",
      "elementId": "btnExpandMarketing",
      "elementType": "button",
      "onclickFunction": "raiseMarketing()",
      "category": "Business"
    },
    {
      "name": "Buy Wire",
      "elementId": "btnBuyWire",
      "elementType": "button",
      "onclickFunction": "buyWire()",
      "category": "Manufacturing"
    },
    {
      "name": "Buy AutoClipper",
      "elementId": "btnMakeClipper",
      "elementType": "button",
      "onclickFunction": "makeClipper()",
      "category": "Manufacturing"
    },
    {
      "name": "Toggle WireBuyer",
      "elementId": "btnToggleWireBuyer",
      "elementType": "button",
      "onclickFunction": "toggleWireBuyer()",
      "category": "Manufacturing"
    },
    {
      "name": "Buy MegaClipper",
      "elementId": "btnMakeMegaClipper",
      "elementType": "button",
      "onclickFunction": "makeMegaClipper()",
      "category": "Manufacturing"
    },
    {
      "name": "Improved AutoClippers",
      "elementId": "btnImproveAutoClippers",
      "elementType": "button",
      "onclickFunction": "improveAutoClippers()",
      "category": "Projects"
    },
    {
      "name": "Beg for More Wire",
      "elementId": "btnBegForWire",
      "elementType": "button",
      "onclickFunction": "begForWire()",
      "category": "Projects"
    },
    {
      "name": "RevTracker",
      "elementId": "btnRevTracker",
      "elementType": "button",
      "onclickFunction": "revTracker()",
      "category": "Projects"
    },
    {
      "name": "Limerick",
      "elementId": "btnLimerick",
      "elementType": "button",
      "onclickFunction": "limerick()",
      "category": "Projects"
    },
    {
      "name": "Deposit Investment",
      "elementId": "btnInvest",
      "elementType": "button",
      "onclickFunction": "invest()",
      "category": "Investments"
    },
    {
      "name": "Withdraw Investment",
      "elementId": "btnWithdraw",
      "elementType": "button",
      "onclickFunction": "withdraw()",
      "category": "Investments"
    },
    {
      "name": "Upgrade Investment Engine",
      "elementId": "btnImproveInvestments",
      "elementType": "button",
      "onclickFunction": "improveInvestments()",
      "category": "Investments"
    },
    {
      "name": "Toggle Strategic Modeling",
      "elementId": "btnToggleStrategicModeling",
      "elementType": "button",
      "onclickFunction": "toggleStrategicModeling()",
      "category": "Strategic Modeling"
    },
    {
      "name": "Run Tournament",
      "elementId": "btnRunTournament",
      "elementType": "button",
      "onclickFunction": "runTournament()",
      "category": "Strategic Modeling"
    },
    {
      "name": "New Tournament",
      "elementId": "btnNewTournament",
      "elementType": "button",
      "onclickFunction": "newTournament()",
      "category": "Strategic Modeling"
    },
    {
      "name": "Toggle AutoTourney",
      "elementId": "btnToggleAutoTourney",
      "elementType": "button",
      "onclickFunction": "toggleAutoTourney()",
      "category": "Strategic Modeling"
    },
    {
      "name": "Launch Probe",
      "elementId": "btnMakeProbe",
      "elementType": "button",
      "onclickFunction": "makeProbe()",
      "category": "Space Exploration"
    },
    {
      "name": "Decrease Probe Speed",
      "elementId": "btnLowerProbeSpeed",
      "elementType": "button",
      "onclickFunction": "lowerProbeSpeed()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Speed",
      "elementId": "btnRaiseProbeSpeed",
      "elementType": "button",
      "onclickFunction": "raiseProbeSpeed()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Exploration",
      "elementId": "btnLowerProbeNav",
      "elementType": "button",
      "onclickFunction": "lowerProbeNav()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Exploration",
      "elementId": "btnRaiseProbeNav",
      "elementType": "button",
      "onclickFunction": "raiseProbeNav()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Self-Replication",
      "elementId": "btnLowerProbeRep",
      "elementType": "button",
      "onclickFunction": "lowerProbeRep()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Self-Replication",
      "elementId": "btnRaiseProbeRep",
      "elementType": "button",
      "onclickFunction": "raiseProbeRep()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Hazard Remediation",
      "elementId": "btnLowerProbeHaz",
      "elementType": "button",
      "onclickFunction": "lowerProbeHaz()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Hazard Remediation",
      "elementId": "btnRaiseProbeHaz",
      "elementType": "button",
      "onclickFunction": "raiseProbeHaz()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Factory Production",
      "elementId": "btnLowerProbeFac",
      "elementType": "button",
      "onclickFunction": "lowerProbeFac()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Factory Production",
      "elementId": "btnRaiseProbeFac",
      "elementType": "button",
      "onclickFunction": "raiseProbeFac()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Harvester Drone Production",
      "elementId": "btnLowerProbeHarv",
      "elementType": "button",
      "onclickFunction": "lowerProbeHarv()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Harvester Drone Production",
      "elementId": "btnRaiseProbeHarv",
      "elementType": "button",
      "onclickFunction": "raiseProbeHarv()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Wire Drone Production",
      "elementId": "btnLowerProbeWire",
      "elementType": "button",
      "onclickFunction": "lowerProbeWire()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Wire Drone Production",
      "elementId": "btnRaiseProbeWire",
      "elementType": "button",
      "onclickFunction": "raiseProbeWire()",
      "category": "Probe Design"
    },
    {
      "name": "Decrease Probe Combat",
      "elementId": "btnLowerProbeCombat",
      "elementType": "button",
      "onclickFunction": "lowerProbeCombat()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Combat",
      "elementId": "btnRaiseProbeCombat",
      "elementType": "button",
      "onclickFunction": "raiseProbeCombat()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Probe Trust",
      "elementId": "btnIncreaseProbeTrust",
      "elementType": "button",
      "onclickFunction": "increaseProbeTrust()",
      "category": "Probe Design"
    },
    {
      "name": "Increase Max Trust",
      "elementId": "btnIncreaseMaxTrust",
      "elementType": "button",
      "onclickFunction": "increaseMaxTrust()",
      "category": "Probe Design"
    },
    {
      "name": "Create Clip Factory",
      "elementId": "btnMakeFactory",
      "elementType": "button",
      "onclickFunction": "makeFactory()",
      "category": "Manufacturing"
    },
    {
      "name": "Disassemble All Factories",
      "elementId": "btnFactoryReboot",
      "elementType": "button",
      "onclickFunction": "factoryReboot()",
      "category": "Manufacturing"
    },
    {
      "name": "Create Harvester Drone",
      "elementId": "btnMakeHarvester",
      "elementType": "button",
      "onclickFunction": "makeHarvester()",
      "category": "Manufacturing"
    },
    {
      "name": "Create Wire Drone",
      "elementId": "btnMakeWireDrone",
      "elementType": "button",
      "onclickFunction": "makeWireDrone()",
      "category": "Manufacturing"
    },
    {
      "name": "Disassemble All Harvester Drones",
      "elementId": "btnHarvesterReboot",
      "elementType": "button",
      "onclickFunction": "harvesterReboot()",
      "category": "Manufacturing"
    },
    {
      "name": "Disassemble All Wire Drones",
      "elementId": "btnWireDroneReboot",
      "elementType": "button",
      "onclickFunction": "wireDroneReboot()",
      "category": "Manufacturing"
    },
    {
      "name": "Create Solar Farm",
      "elementId": "btnMakeFarm",
      "elementType": "button",
      "onclickFunction": "makeFarm()",
      "category": "Power"
    },
    {
      "name": "Disassemble All Solar Farms",
      "elementId": "btnFarmReboot",
      "elementType": "button",
      "onclickFunction": "farmReboot()",
      "category": "Power"
    },
    {
      "name": "Create Battery Tower",
      "elementId": "btnMakeBattery",
      "elementType": "button",
      "onclickFunction": "makeBattery()",
      "category": "Power"
    },
    {
      "name": "Disassemble All Battery Towers",
      "elementId": "btnBatteryReboot",
      "elementType": "button",
      "onclickFunction": "batteryReboot()",
      "category": "Power"
    },
    {
      "name": "Swarm Computing: Feed",
      "elementId": "btnFeedSwarm",
      "elementType": "button",
      "onclickFunction": "feedSwarm()",
      "category": "Swarm Computing"
    },
    {
      "name": "Swarm Computing: Teach",
      "elementId": "btnTeachSwarm",
      "elementType": "button",
      "onclickFunction": "teachSwarm()",
      "category": "Swarm Computing"
    },
    {
      "name": "Swarm Computing: Entertain",
      "elementId": "btnEntertainSwarm",
      "elementType": "button",
      "onclickFunction": "entertainSwarm()",
      "category": "Swarm Computing"
    },
    {
      "name": "Swarm Computing: Clad",
      "elementId": "btnCladSwarm",
      "elementType": "button",
      "onclickFunction": "cladSwarm()",
      "category": "Swarm Computing"
    },
    {
      "name": "Swarm Computing: Synchronize",
      "elementId": "btnSynchSwarm",
      "elementType": "button",
      "onclickFunction": "synchSwarm()",
      "category": "Swarm Computing"
    },
    {
      "name": "Quantum Computing",
      "elementId": "btnQcompute",
      "elementType": "button",
      "onclickFunction": "qComp()",
      "category": "Quantum Computing"
    }
  ]
}

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
            model="gpt-4o-mini",
            messages=self.messages[:1]
            + [message for message in self.messages if message["role"] == "assistant"]
            + self.messages[-1:],
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        logger.info(f"Token usage: {completion.usage}")
        return completion.choices[0].message.content


def main(max_turns=30):
    # Set up ChromeDriver
    action_re = re.compile("Action: (\w+): <javascript>(.*?)</javascript>", re.DOTALL)

    i = 0
    bot = ChatBot(system=prompt)
    next_prompt = f"Observation: Game Started ! \n  Current Game State: {observation()} \n Current Javascript Strategy: null"
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        logger.info(result)
        actions = action_re.findall(result)

        if actions:
            # There is an action to run
            action, action_input = actions[0]
            if action not in known_actions.keys():
                logger.error(f"Unknown action: {action}: {action_input}")
                raise Exception(f"Unknown action: {action}: {action_input}")
            logger.info(f"Running {action} {action_input}")
            observations = known_actions[action](action_input)
            logger.info(f"Observation: {observations}")
            next_prompt = (
                f"Observation: {observations} \n Current Game State: {observation()}"
            )
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
        return digest()
    except Exception as e:
        logger.error(f"Error during observation: {e}")
        return None

def digest():
    """
    Digests the current state of the game by fetching the entire HTML of the page
    and running it through the unstructured partioning model."""
    try:
        html_content = driver.page_source.replace("\n", "")
        elements = partition_html(text=html_content)
        text = "\n\n".join([str(el) for el in elements])
        logger.info(f"Digestion: {text}")
        return text
    except Exception as e:
        logger.error(f"Error during digestion: {e}")
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
            window.activeStrategyInterval = setInterval(() => { %s }, 150);
            console.log('New strategy set');
            """
            % strategy_script
        )
        return "Strategy replaced successfully"
    except Exception as e:
        logger.error(f"Error executing strategy: {e}")
        return None


known_actions = {
    "ModifyJavascriptStrategy": modify_javascript_strategy,
}

if __name__ == "__main__":
    main()
