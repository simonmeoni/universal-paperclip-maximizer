import re

from environment import Environment


class Tools:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.action_re = re.compile(r"Action: (.+): (.+)")

    def __call__(self, action, action_input, environment: Environment):
        if action in environment.actions_available:
            for _ in range(int(action_input)):
                self.driver.execute_script(environment.actions_available[action])
                self.logger.info(f"Executing action: {action}")
            return f"Action: {action}: {action_input} was successfully executed"
        else:
            self.logger.warning(
                f"Action: {action}: {action_input} is not a valid action"
            )
            return f"Action: {action}: {action_input} is not a valid action"
