import re


class Tools:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.action_re = re.compile(r"Action: (.+): (.+)")
        self.all_tools = {
            # Manufacturing tools
            "Make Paperclip": lambda: self.execute_action_input("btnMakePaperclip", "click()"),
            "Buy Wire": lambda: self.execute_action_input("btnBuyWire", "click()"),
            "Buy AutoClipper": lambda: self.execute_action_input("btnMakeClipper", "click()"),
            "Toggle WireBuyer": lambda: self.execute_action_input("btnToggleWireBuyer", "click()"),
            "Buy MegaClipper": lambda: self.execute_action_input("btnMakeMegaClipper", "click()"),
            "Create Clip Factory": lambda: self.execute_action_input("btnMakeFactory", "click()"),
            "Disassemble All Factories": lambda: self.execute_action_input("btnFactoryReboot", "click()"),
            "Create Harvester Drone": lambda: self.execute_action_input("btnMakeHarvester", "click()"),
            "Create Wire Drone": lambda: self.execute_action_input("btnMakeWireDrone", "click()"),
            "Disassemble All Harvester Drones": lambda: self.execute_action_input("btnHarvesterReboot", "click()"),
            "Disassemble All Wire Drones": lambda: self.execute_action_input("btnWireDroneReboot", "click()"),

            # Business tools
            "Lower Price": lambda: self.execute_action_input("btnLowerPrice", "click()"),
            "Raise Price": lambda: self.execute_action_input("btnRaisePrice", "click()"),
            "Upgrade Marketing": lambda: self.execute_action_input("btnExpandMarketing", "click()"),

            # Projects tools
            "Improved AutoClippers": lambda: self.execute_action_input("btnImproveAutoClippers", "click()"),
            "Beg for More Wire": lambda: self.execute_action_input("projectButton2", "click()"),
            "RevTracker": lambda: self.execute_action_input("btnRevTracker", "click()"),
            "Limerick": lambda: self.execute_action_input("btnLimerick", "click()"),

            # Investments tools
            "Deposit Investment": lambda: self.execute_action_input("btnInvest", "click()"),
            "Withdraw Investment": lambda: self.execute_action_input("btnWithdraw", "click()"),
            "Upgrade Investment Engine": lambda: self.execute_action_input("btnImproveInvestments", "click()"),

            # Strategic modeling tools
            "Toggle Strategic Modeling": lambda: self.execute_action_input("btnToggleStrategicModeling", "click()"),
            "Run Tournament": lambda: self.execute_action_input("btnRunTournament", "click()"),
            "New Tournament": lambda: self.execute_action_input("btnNewTournament", "click()"),
            "Toggle AutoTourney": lambda: self.execute_action_input("btnToggleAutoTourney", "click()"),

            # Space exploration tools
            "Launch Probe": lambda: self.execute_action_input("btnMakeProbe", "click()"),

            # Probe design tools
            "Decrease Probe Speed": lambda: self.execute_action_input("btnLowerProbeSpeed", "click()"),
            "Increase Probe Speed": lambda: self.execute_action_input("btnRaiseProbeSpeed", "click()"),
            "Decrease Probe Exploration": lambda: self.execute_action_input("btnLowerProbeNav", "click()"),
            "Increase Probe Exploration": lambda: self.execute_action_input("btnRaiseProbeNav", "click()"),
            "Decrease Probe Self-Replication": lambda: self.execute_action_input("btnLowerProbeRep", "click()"),
            "Increase Probe Self-Replication": lambda: self.execute_action_input("btnRaiseProbeRep", "click()"),
            "Decrease Probe Hazard Remediation": lambda: self.execute_action_input("btnLowerProbeHaz", "click()"),
            "Increase Probe Hazard Remediation": lambda: self.execute_action_input("btnRaiseProbeHaz", "click()"),
            "Decrease Probe Factory Production": lambda: self.execute_action_input("btnLowerProbeFac", "click()"),
            "Increase Probe Factory Production": lambda: self.execute_action_input("btnRaiseProbeFac", "click()"),
            "Decrease Probe Harvester Drone Production": lambda: self.execute_action_input("btnLowerProbeHarv", "click()"),
            "Increase Probe Harvester Drone Production": lambda: self.execute_action_input("btnRaiseProbeHarv", "click()"),
            "Decrease Probe Wire Drone Production": lambda: self.execute_action_input("btnLowerProbeWire", "click()"),
            "Increase Probe Wire Drone Production": lambda: self.execute_action_input("btnRaiseProbeWire", "click()"),
            "Decrease Probe Combat": lambda: self.execute_action_input("btnLowerProbeCombat", "click()"),
            "Increase Probe Combat": lambda: self.execute_action_input("btnRaiseProbeCombat", "click()"),
            "Increase Probe Trust": lambda: self.execute_action_input("btnIncreaseProbeTrust", "click()"),
            "Increase Max Trust": lambda: self.execute_action_input("btnIncreaseMaxTrust", "click()"),

            # Power tools
            "Create Solar Farm": lambda: self.execute_action_input("btnMakeFarm", "click()"),
            "Disassemble All Solar Farms": lambda: self.execute_action_input("btnFarmReboot", "click()"),
            "Create Battery Tower": lambda: self.execute_action_input("btnMakeBattery", "click()"),
            "Disassemble All Battery Towers": lambda: self.execute_action_input("btnBatteryReboot", "click()"),

            # Swarm computing tools
            "Swarm Computing: Feed": lambda: self.execute_action_input("btnFeedSwarm", "click()"),
            "Swarm Computing: Teach": lambda: self.execute_action_input("btnTeachSwarm", "click()"),
            "Swarm Computing: Entertain": lambda: self.execute_action_input("btnEntertainSwarm", "click()"),
            "Swarm Computing: Clad": lambda: self.execute_action_input("btnCladSwarm", "click()"),
            "Swarm Computing: Synchronize": lambda: self.execute_action_input("btnSynchSwarm", "click()"),

            # Quantum computing tools
            "Quantum Computing": lambda: self.execute_action_input("btnQcompute", "click()"),
        }



    def execute_action_input(self, element_id, function_name):
        """
        Executes a specified action by interacting with a button on the webpage using the provided elementId.
        """

        try:
            self.driver.execute_script(
                f"document.getElementById('{element_id}').{function_name}"
            )
            self.logger.info(
                f"Executed action: {function_name} on element: {element_id}"
            )
            return f"Action {function_name} executed successfully."
        except Exception as e:
            self.logger.error(f"Error executing action {function_name}: {e}")
            return None

    def __call__(self, action_input):
        self.all_tools[action_input]()