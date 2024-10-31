from selenium.webdriver.common.by import By


class Environment:
    def __init__(self, driver, logger):
        # Initialize any necessary attributes here
        self.driver = driver
        self.logger = logger
        self.actions_available = {}

    def get_game_state(self):
        """
        Observes the current state of the game by fetching the entire HTML of the page.
        Returns the HTML as a string.
        """
        try:
            html_content = self.driver.page_source.replace("\n", "")
            return (
                f"**Game State:**\n {self.digest(html_content)} \n"
                f"**Action Available:**\n {self.get_actions().strip()}"
            )
        except Exception as e:
            self.logger.error(f"Error during observation: {e}")
            return None

    def get_actions(self):
        """
        Finds the available actions in the HTML content.
        Returns a list of JavaScript functions from button attributes.
        """
        self.actions_available = {}
        try:
            # Find all button elements
            button_elements = self.driver.find_elements("tag name", "button")
            actions = []
            for element in button_elements:
                if element.is_displayed() and element.is_enabled():
                    if "projectButton" in element.get_attribute("class"):
                        element_id = element.get_attribute("id")
                        title = element.text.split("(")[0].strip()
                        actions.append(title)
                        self.actions_available[title] = f"document.getElementById('{element_id}').click()"
                    else:
                        onclick_attr = element.get_attribute("onclick")
                        button_name = element.text
                        if onclick_attr:
                            actions.append(button_name)
                            self.actions_available[
                                button_name] = onclick_attr
            return "\n".join(actions)
        except Exception as e:
            self.logger.error(f"Error during finding actions: {e}")
            return None

    def digest(self, html_content):
        """
        Digests the current state of the game by fetching the entire HTML of the page
        and running it through the unstructured partioning model."""
        # Sample body text
        return "\n***************\n".join(
             [self.driver.find_element("id", "readout1").text] + [
                div.text
                for div in self.driver.find_elements(By.XPATH, "*/*/*/*/div")
                if div.text != ""
            ][1:]
        )
