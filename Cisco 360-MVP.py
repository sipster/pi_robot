import time
import random

# --- CONFIGURATION & WEIGHTS (Based on File-3) ---
PORTFOLIO_WEIGHTS = {
    "Security": {"perf": 0.25, "cap": 0.45, "found": 0.30, "eng": 0.00},
    "Networking": {"perf": 0.25, "cap": 0.25, "found": 0.25, "eng": 0.25}
}

# Archetypes: [Performance, Capabilities, Foundational, Engagement]
ARCHETYPES = {
    "1": {"name": "Legacy Reseller", "stats": [7.0, 2.0, 1.0, 2.0]},
    "2": {"name": "Emerging MSP", "stats": [3.0, 3.0, 6.0, 2.0]},
    "3": {"name": "Security Specialist", "stats": [4.0, 8.0, 2.0, 3.0]}
}

# --- UI COLORS ---
class Color:
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# --- GAME ENGINE ---
class Cisco360Game:
    def __init__(self):
        self.quarter = 1
        self.partner_name = ""
        self.stats = [0, 0, 0, 0] # Perf, Cap, Found, Eng
        self.pvi = 0.0
        self.portfolio = "Security"
        self.rebates = 0

    def clear_screen(self):
        print("\n" * 50)

    def header(self):
        print(f"{Color.CYAN}{Color.BOLD}=== CISCO 360: THE PATH TO PREFERRED ==={Color.END}")
        print(f"Quarter: Q{self.quarter} | Portfolio: {self.portfolio} | Status: {self.get_status_text()}")
        print("-" * 50)

    def get_status_text(self):
        if self.pvi >= 7.5: return f"{Color.GOLD}CISCO PREFERRED PARTNER{Color.END}"
        if self.pvi >= 5.0: return f"{Color.GREEN}CISCO PORTFOLIO PARTNER{Color.END}"
        return f"{Color.RED}BASE PARTNER{Color.END}"

    def calculate_pvi(self):
        w = PORTFOLIO_WEIGHTS[self.portfolio]
        self.pvi = (self.stats[0] * w["perf"]) + (self.stats[1] * w["cap"]) + \
                   (self.stats[2] * w["found"]) + (self.stats[3] * w["eng"])
        return round(self.pvi, 2)

    def start_game(self):
        self.clear_screen()
        print(f"{Color.CYAN}Initializing Cisco 360 Partner Portal...{Color.END}")
        time.sleep(1)
        self.partner_name = input("\nEnter your Partner Organization Name: ")
        
        print("\nSelect your Partner Archetype (Starting Baseline):")
        for k, v in ARCHETYPES.items():
            print(f"{k}) {v['name']} (Initial PVI: {sum(v['stats'])/4})")
        
        choice = input("\nChoice [1-3]: ")
        self.stats = ARCHETYPES[choice]["stats"]
        self.calculate_pvi()

    def play_quarter(self):
        self.clear_screen()
        self.header()
        print(f"Current {self.portfolio} PVI: {Color.BOLD}{self.pvi}{Color.END}")
        print(f"Stats: Perf[{self.stats[0]}] Cap[{self.stats[1]}] Found[{self.stats[2]}] Eng[{self.stats[3]}]")
        print("\nChoose your Strategic Action for this Quarter:")
        
        actions = [
            ("1", "Enroll Engineering team in Black Belt Academy", [0, 2.0, 0, 0], "Boosts Capabilities"),
            ("2", "Conduct a Customer Security Assessment (PXP)", [0.5, 0, 0, 2.5], "Boosts Engagement & Performance"),
            ("3", "Upgrade Managed Services Practice Maturity (Audit)", [0, 0, 3.0, 0], "Boosts Foundational"),
            ("4", "Migrate Customer to Enterprise Agreement (EA)", [2.5, 0, 0, 0], "Boosts Performance")
        ]

        for cmd, name, _, desc in actions:
            print(f"{cmd}) {Color.BOLD}{name}{Color.END} - {desc}")

        move = input("\nSelect Action: ")
        
        # Apply Stats
        for cmd, name, impact, _ in actions:
            if move == cmd:
                print(f"\n{Color.GREEN}Executing: {name}...{Color.END}")
                for i in range(4): self.stats[i] += impact[i]
                time.sleep(1.5)

        self.calculate_pvi()
        self.quarter += 1

    def final_results(self):
        self.clear_screen()
        print(f"{Color.CYAN}{Color.BOLD}=== FISCAL YEAR END SUMMARY: {self.partner_name} ==={Color.END}")
        print(f"Final PVI Score: {self.pvi}")
        
        if self.pvi >= 7.5:
            print(f"\n{Color.GOLD}CONGRATULATIONS! You are a Cisco Preferred Partner.{Color.END}")
            print("You have unlocked:")
            print("- Maximum Land/Adopt/Grow Rebates")
            print("- Next-Generation Specialization Eligibility")
            print("- 10 Annual Cisco U. Licenses")
        elif self.pvi >= 5.0:
            print(f"\n{Color.GREEN}SUCCESS! You are a Cisco Portfolio Partner.{Color.END}")
            print("You have unlocked:")
            print("- Cisco Partner Incentive (Base Rebates)")
            print("- Customer Assessment Incentives")
        else:
            print(f"\n{Color.RED}ALERT: You remain a Base Partner.{Color.END}")
            print("Action Required: Increase Capabilities or Practice Maturity to unlock incentives.")
        
        print(f"\n{Color.CYAN}Final Stats: Perf:{self.stats[0]} | Cap:{self.stats[1]} | Found:{self.stats[2]} | Eng:{self.stats[3]}{Color.END}")
        print("\nThank you for playing the Cisco 360 Path to Preferred.")

# --- RUN GAME ---
if __name__ == "__main__":
    game = Cisco360Game()
    game.start_game()
    
    while game.quarter <= 4:
        game.play_quarter()
    
    game.final_results()