import re


class Tools:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.known_actions = {
            "ModifyJavascriptStrategy": self.modify_javascript_strategy,
        }
        self.action_re = re.compile(r"Action: (\w+): <javascript>(.*?)</javascript>", re.DOTALL)

    def modify_javascript_strategy(self, strategy_script):
        """
        Modifies the JavaScript strategy by replacing the old one if it exists.
        Returns the result of the operation.
        """
        try:
            # JavaScript to check if a strategy already exists and clear it if needed
            self.driver.execute_script(
                """
                // Check if a previous strategy exists and clear the interval
                if (window.activeStrategyInterval) {
                    clearInterval(window.activeStrategyInterval);
                    console.log('Previous strategy cleared');
                }

                // Set the new strategy with setInterval and store it globally
                %s
                console.log('New strategy set');
                """
                % strategy_script
            )
            return "Strategy replaced successfully"
        except Exception as e:
            self.logger.error(f"Error executing strategy: {e}")
            return None