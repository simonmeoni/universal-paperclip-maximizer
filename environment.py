import re

# If the 'unstructured' package is not installed, you may need to install it using:
# pip install unstructured


class Environment:
    def __init__(self, driver, logger):
        # Initialize any necessary attributes here
        self.driver = driver
        self.logger = logger

    def observation(self):
        """
        Observes the current state of the game by fetching the entire HTML of the page.
        Returns the HTML as a string.
        """
        try:
            html_content = self.driver.page_source.replace("\n", "")
            return (f"**Digest:**\n {self.digest(html_content)} \n\n "
                    f"**Action Available:**\n {self.find_action(html_content)}")
        except Exception as e:
            self.logger.error(f"Error during observation: {e}")
            return None

    def find_action(self, html_content):
        """
        Finds the available actions in the HTML content.
        Returns a list of JavaScript functions from button attributes.
        """
        try:
            # Find all button elements
            button_elements = self.driver.find_elements("tag name", "button")
            actions = []
            for element in button_elements:
                if element.is_displayed() and element.is_enabled():
                    if "projectButton" in element.get_attribute("class"):
                        element_id = element.get_attribute("id")
                        actions.append(
                            f"{element.text}: document.getElementById('{element_id}').click()"
                        )
                    else:
                        onclick_attr = element.get_attribute("onclick")
                        button_name = element.text
                        if onclick_attr:
                            actions.append(f"{button_name}: {onclick_attr}")
            return "\n".join(actions)
        except Exception as e:
            self.logger.error(f"Error during finding actions: {e}")
            return None

    def digest(self, html_content):
        """
        Digests the current state of the game by fetching the entire HTML of the page
        and running it through the unstructured partioning model."""
        # Sample body text
        body_text = self.driver.find_element("tag name", "body").text

        # Clean up the text

        # Step 1: Remove multiple newlines and extra spaces
        cleaned_text = re.sub(
            r"\n+", "\n", body_text
        )  # Collapse multiple newlines into a single one
        cleaned_text = re.sub(
            r" {2,}", " ", cleaned_text
        )  # Collapse multiple spaces into a single space

        # Step 2: Optionally, remove unwanted sections
        # For example, removing lines that include "Mobile Version", "T-Shirts", and other irrelevant sections
        lines = cleaned_text.splitlines()
        relevant_lines = []
        for line in lines:
            if not any(
                phrase in line for phrase in ["Mobile Version", "T-Shirts", "...", "|"]
            ):
                relevant_lines.append(line.strip())

        # Join the relevant lines back into a single string
        final_cleaned_text = "\n".join(relevant_lines)
        return final_cleaned_text
