import re

class Tools:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.action_re = re.compile(r"Action: (.+): (.+)")
        self.list_action_re = re.compile(r"\[(.+)\]")

    def __call__(self, action_input):
        self.driver.execute_script(f"{action_input}")
        self.logger.info(f"Executing action: {action_input}")
