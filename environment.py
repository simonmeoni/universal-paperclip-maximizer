from unstructured.partition.html import partition_html

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
            return html_content
        except Exception as e:
            self.logger.error(f"Error during observation: {e}")
            return None

    def digest(self, html_content):
        """
        Digests the current state of the game by fetching the entire HTML of the page
        and running it through the unstructured partioning model."""
        try:
            elements = partition_html(text=html_content)
            text = "\n\n".join([str(el) for el in elements])
            self.logger.info(f"Digestion: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error during digestion: {e}")
            return None
