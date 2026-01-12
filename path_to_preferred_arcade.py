import os
import time
from typing import List, Tuple

# ------------------------------------------------------------
#  COLORS / STYLES (ANSI)
# ------------------------------------------------------------
class UI:
    CYAN = "\033[96m"
    GOLD = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# ------------------------------------------------------------
#  DATA & WEIGHTS
# ------------------------------------------------------------
SECURITY_WEIGHTS = {"perf": 0.25, "cap": 0.45, "found": 0.30, "eng": 0.00}

ARCHETYPES = {
    "1": {
        "name": "THE RESELLER",
        "desc": "High sales volume, but lacks technical depth.",
        "stats": [7.0, 2.0, 1.0, 2.0],
    },
    "2": {
        "name": "THE MSP",
        "desc": "Strong managed services, but needs to scale sales.",
        "stats": [3.0, 3.0, 7.0, 2.0],
    },
    "3": {
        "name": "THE SPECIALIST",
        "desc": "Technical gurus, but needs more recurring revenue.",
        "stats": [4.0, 8.0, 2.0, 3.0],
    },
}


# ------------------------------------------------------------
#  HELPER FUNCTIONS
# ------------------------------------------------------------
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text: str, delay: float = 0.015) -> None:
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def bar(value: float, width: int = 24) -> str:
    filled = int((value / 10) * width)
    filled = max(0, min(width, filled))
    return f"{UI.GREEN}{'█' * filled}{UI.RED}{'░' * (width - filled)}{UI.END}"


def colored_status(pvi: float) -> Tuple[str, str]:
    if pvi >= 7.5:
        return f"{UI.GOLD}CISCO PREFERRED{UI.END}", UI.GOLD
    if pvi >= 5.0:
        return f"{UI.GREEN}CISCO PORTFOLIO{UI.END}", UI.GREEN
    return f"{UI.RED}BASE PARTNER{UI.END}", UI.RED


def prompt_choice(prompt: str, valid: List[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid:
            return choice
        print(f"{UI.RED}Invalid choice. Try again.{UI.END}")


# ------------------------------------------------------------
#  GAME ENGINE
# ------------------------------------------------------------
class PathToPreferredArcade:
    def __init__(self) -> None:
        self.partner_name = ""
        self.stats = [0.0, 0.0, 0.0, 0.0]  # Perf, Cap, Found, Eng
        self.pvi = 0.0
        self.quarter = 1
        self.status = "BASE PARTNER"

    # ------------- UI RENDERING -------------
    def render_banner(self) -> None:
        banner = f"""
{UI.CYAN}{UI.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║   ____ ___ ____   ____ ___      ____  __  __    _    ____   ____      ║
║  / ___|_ _/ ___| / ___/ _ \\    / ___||  \\/  |  / \\  |  _ \\ / ___|     ║
║ | |    | |\\___ \\| |  | | | |   \\___ \\| |\\/| | / _ \\ | |_) | |         ║
║ | |___ | | ___) | |__| |_| |    ___) | |  | |/ ___ \\|  __/| |___      ║
║  \\____|___|____/ \\____\\___/    |____/|_|  |_/_/   \\_\\_|    \\____|     ║
║                                                                      ║
║          T H E   P A T H   T O   P R E F E R R E D   A R C A D E     ║
╚══════════════════════════════════════════════════════════════════════╝{UI.END}
"""
        print(banner)

    def render_dashboard(self) -> None:
        clear_screen()
        self.render_banner()

        status_text, status_color = colored_status(self.pvi)

        print(
            f"{UI.MAGENTA}{UI.BOLD}QUARTER Q{self.quarter}{UI.END}   "
            f"{UI.BOLD}PARTNER:{UI.END} {self.partner_name[:18]:<18}   "
            f"{UI.BOLD}PORTFOLIO:{UI.END} SECURITY"
        )
        print("═" * 70)
        labels = ["PERFORMANCE", "CAPABILITIES", "FOUNDATIONAL", "ENGAGEMENT"]
        for label, value in zip(labels, self.stats):
            print(
                f"{UI.WHITE}{label:<15}{UI.END} {value:>4.1f}/10  {bar(value)}"
            )
        print("═" * 70)
        print(
            f"{UI.BOLD}CURRENT PVI:{UI.END} {status_color}{self.pvi:<4.1f}{UI.END}   "
            f"{UI.BOLD}STATUS:{UI.END} {status_text}"
        )
        print("═" * 70)

    # ------------- GAME LOGIC -------------
    def update_pvi(self) -> None:
        w = SECURITY_WEIGHTS
        self.pvi = round(
            (self.stats[0] * w["perf"])
            + (self.stats[1] * w["cap"])
            + (self.stats[2] * w["found"])
            + (self.stats[3] * w["eng"]),
            2,
        )
        self.status, _ = colored_status(self.pvi)

    def intro(self) -> None:
        clear_screen()
        self.render_banner()
        slow_print(f"{UI.WHITE}BOOTING CISCO 360 MAINFRAME...{UI.END}", 0.01)
        slow_print(f"{UI.GREEN}ONLINE. WELCOME, ALLIANCE MANAGER.{UI.END}", 0.01)
        print("\n" + "═" * 70)
        slow_print(
            f"{UI.BOLD}MISSION:{UI.END} Navigate 4 quarters and hit PVI 7.5 for "
            "CISCO PREFERRED status."
        )
        slow_print(
            "Pro tip: In Security, Capabilities (45%) and Foundational (30%) "
            "carry the weight. Engagement has no weight here."
        )
        print("═" * 70)
        input(f"\nPress {UI.GREEN}[ENTER]{UI.END} to begin the simulation...")

    def choose_archetype(self) -> None:
        clear_screen()
        self.render_banner()
        print(f"{UI.BOLD}SELECT YOUR STARTING ARCHETYPE:{UI.END}\n")
        for key, data in ARCHETYPES.items():
            print(f"{key}. {UI.CYAN}{data['name']}{UI.END} - {data['desc']}")
        choice = prompt_choice("\nChoice [1-3]: ", list(ARCHETYPES.keys()))
        self.partner_name = input(
            f"\n{UI.BOLD}ENTER FIRM NAME:{UI.END} "
        ).strip().upper() or "ALLY PARTNER"
        self.stats = ARCHETYPES[choice]["stats"][:]
        self.update_pvi()

    def play_quarter(
        self,
        story: str,
        options: List[Tuple[str, List[float], str]],
    ) -> None:
        self.render_dashboard()
        print(f"{UI.BOLD}STORY:{UI.END} {story}\n")
        for idx, (text, _, impact_desc) in enumerate(options, start=1):
            print(f"{idx}. {text} {UI.GREEN}({impact_desc}){UI.END}")

        choice = int(prompt_choice(f"\n{UI.BOLD}COMMAND?{UI.END} ", ["1", "2"])) - 1
        impact = options[choice][1]
        for i in range(4):
            self.stats[i] += impact[i]

        print(f"\n{UI.CYAN}PROCESSING DATA...{UI.END}")
        time.sleep(1.2)
        self.update_pvi()
        self.quarter += 1

    def finale(self) -> None:
        self.render_dashboard()
        if self.pvi >= 7.5:
            print(
                f"{UI.GOLD}╔══════════════════════════════════════════════════════════════════╗"
            )
            print(
                "║ MISSION COMPLETE: CISCO PREFERRED STATUS UNLOCKED.               ║"
            )
            print(
                "║ Maximum Rebates | Next-Gen Specializations | 10 Cisco U Licenses  ║"
            )
            print(
                f"╚══════════════════════════════════════════════════════════════════╝{UI.END}"
            )
        elif self.pvi >= 5.0:
            print(
                f"{UI.GREEN}╔══════════════════════════════════════════════════════════════════╗"
            )
            print(
                "║ PORTFOLIO STATUS ACHIEVED. PUSH CAPABILITIES TO HIT PREFERRED.   ║"
            )
            print(
                f"╚══════════════════════════════════════════════════════════════════╝{UI.END}"
            )
        else:
            print(
                f"{UI.RED}╔══════════════════════════════════════════════════════════════════╗"
            )
            print(
                "║ MISSION FAILED. STRENGTHEN CAPABILITIES & FOUNDATIONAL PRACTICE. ║"
            )
            print(
                f"╚══════════════════════════════════════════════════════════════════╝{UI.END}"
            )
        print(f"\n{UI.BOLD}Final PVI: {self.pvi}{UI.END}")
        print(f"{UI.WHITE}Thank you for playing the Cisco 360 Arcade Simulation.{UI.END}")

    # ------------- ENTRY POINT -------------
    def run(self) -> None:
        self.intro()
        self.choose_archetype()

        scenarios = [
            (
                "Q1: THE TALENT WAR. A rival is poaching your engineers.",
                [
                    (
                        "Invest in Black Belt Academy certifications.",
                        [0, 2.5, 0, 0],
                        "Cap +2.5",
                    ),
                    (
                        "Focus on aggressive sales to offset losses.",
                        [2.0, 0, 0, 0],
                        "Perf +2.0",
                    ),
                ],
            ),
            (
                "Q2: THE MSP PIVOT. Cisco 360 rewards Practice Maturity.",
                [
                    (
                        "Undergo an Expert Managed Services Audit.",
                        [0, 0, 3.0, 0],
                        "Found +3.0",
                    ),
                    (
                        "Launch a Customer Success 'Adopt' campaign.",
                        [0, 0, 0, 3.0],
                        "Eng +3.0",
                    ),
                ],
            ),
            (
                "Q3: THE SECURITY BOOM. Customers ask for XDR.",
                [
                    (
                        "Run a Customer Assessment Incentive (CAI) deep-dive.",
                        [1.0, 0, 0, 2.0],
                        "Perf +1, Eng +2",
                    ),
                    (
                        "Achieve the Next-Gen Security Specialization.",
                        [0, 3.0, 0, 0],
                        "Cap +3.0",
                    ),
                ],
            ),
            (
                "Q4: THE FINAL PUSH. Fiscal year end is approaching.",
                [
                    (
                        "Close a massive Enterprise Agreement (EA) deal.",
                        [3.0, 0, 0, 0],
                        "Perf +3.0",
                    ),
                    (
                        "Cross-sell Splunk into the Security base.",
                        [1.5, 1.5, 0, 0],
                        "Perf +1.5, Cap +1.5",
                    ),
                ],
            ),
        ]

        for story, options in scenarios:
            self.play_quarter(story, options)

        self.finale()


if __name__ == "__main__":
    game = PathToPreferredArcade()
    game.run()
