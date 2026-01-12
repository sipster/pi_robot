import math
import sys
from typing import Dict, List, Tuple

import pygame

# ------------------------------------------------------------
#  GAME CONSTANTS
# ------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
FPS = 60

DASHBOARD_HEIGHT = HEIGHT // 4  # bottom quarter of the screen
VIEWPORT_HEIGHT = HEIGHT - DASHBOARD_HEIGHT

BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
CYAN = (0, 220, 255)
GOLD = (255, 215, 0)
GREEN = (0, 230, 140)
RED = (230, 30, 70)
PURPLE = (180, 0, 255)
BLUE = (70, 150, 255)
GRAY = (30, 30, 40)
DARK_GRAY = (10, 10, 20)


# ------------------------------------------------------------
#  DATA & WEIGHTS
# ------------------------------------------------------------
PORTFOLIO_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Security": {"perf": 0.25, "cap": 0.45, "found": 0.30, "eng": 0.00},
    "Networking": {"perf": 0.25, "cap": 0.25, "found": 0.25, "eng": 0.25},
}

CHARACTERS = [
    {
        "name": "Riley 'The Reseller'",
        "archetype": "High-velocity deal maker, light on services depth.",
        "stats": [7.0, 2.0, 1.0, 2.0],
    },
    {
        "name": "Morgan 'The MSP'",
        "archetype": "Managed services machine, needs to scale sales.",
        "stats": [3.0, 3.0, 7.0, 2.0],
    },
    {
        "name": "Alex 'The Specialist'",
        "archetype": "Security guru, hungry for recurring revenue.",
        "stats": [4.0, 8.0, 2.0, 3.0],
    },
]

SCENARIOS = [
    {
        "title": "Q1: THE TALENT WAR",
        "text": "A rival is poaching your top security engineers.",
        "options": [
            (
                "Invest in deep Black Belt Academy training.",
                [0.0, 2.5, 0.0, 0.0],
                "Capabilities +2.5",
            ),
            (
                "Double down on aggressive short-term sales.",
                [2.0, 0.0, 0.0, 0.0],
                "Performance +2.0",
            ),
        ],
    },
    {
        "title": "Q2: THE MSP PIVOT",
        "text": "Cisco 360 is rewarding partners with mature practices.",
        "options": [
            (
                "Undergo an Expert Managed Services Audit.",
                [0.0, 0.0, 3.0, 0.0],
                "Foundational +3.0",
            ),
            (
                "Launch a customer success 'Adopt' wave.",
                [0.0, 0.0, 0.0, 3.0],
                "Engagement +3.0",
            ),
        ],
    },
    {
        "title": "Q3: THE SECURITY BOOM",
        "text": "Customers are asking for XDR and zero trust outcomes.",
        "options": [
            (
                "Run a Customer Assessment Incentive (CAI) deep-dive.",
                [1.0, 0.0, 0.0, 2.0],
                "Perf +1.0, Eng +2.0",
            ),
            (
                "Achieve Next-Gen Security Specialization.",
                [0.0, 3.0, 0.0, 0.0],
                "Capabilities +3.0",
            ),
        ],
    },
    {
        "title": "Q4: THE FINAL PUSH",
        "text": "Fiscal year end is approaching fast.",
        "options": [
            (
                "Close a massive Enterprise Agreement (EA) deal.",
                [3.0, 0.0, 0.0, 0.0],
                "Performance +3.0",
            ),
            (
                "Cross-sell Splunk into your security base.",
                [1.5, 1.5, 0.0, 0.0],
                "Perf +1.5, Cap +1.5",
            ),
        ],
    },
]


# ------------------------------------------------------------
#  PYGAME SETUP
# ------------------------------------------------------------
pygame.init()
pygame.display.set_caption("Cisco 360 / Path to Preferred Partner Adventure")

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont("Arial", 52, bold=True)
BIG_FONT = pygame.font.SysFont("Arial", 40, bold=True)
MED_FONT = pygame.font.SysFont("Arial", 28, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 20)


def draw_text_center(text: str, font: pygame.font.Font, color, surface, y: int):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    surface.blit(rendered, rect)


def draw_button(
    text: str,
    rect: pygame.Rect,
    hover: bool,
    surface,
    base_color,
    hover_color,
):
    color = hover_color if hover else base_color
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)
    label = MED_FONT.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)


def interpolate_color(c1, c2, t: float):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def compute_pvi(stats: List[float], portfolio: str) -> float:
    w = PORTFOLIO_WEIGHTS[portfolio]
    perf, cap, found, eng = stats
    pvi = (
        perf * w["perf"]
        + cap * w["cap"]
        + found * w["found"]
        + eng * w["eng"]
    )
    return round(pvi, 2)


def pvi_tier(pvi: float) -> Tuple[str, Tuple[int, int, int]]:
    if pvi >= 7.5:
        return "CISCO PREFERRED", GOLD
    if pvi >= 5.0:
        return "CISCO PORTFOLIO", GREEN
    return "BASE PARTNER", RED


def draw_dashboard(
    surface,
    stats: List[float],
    portfolio: str,
    quarter: int,
    pvi: float,
    character_name: str,
):
    dash_rect = pygame.Rect(0, VIEWPORT_HEIGHT, WIDTH, DASHBOARD_HEIGHT)
    pygame.draw.rect(surface, GRAY, dash_rect)
    pygame.draw.rect(surface, DARK_GRAY, dash_rect, 4)

    tier_text, tier_color = pvi_tier(pvi)

    # Top row: titles
    label = SMALL_FONT.render(
        f"Quarter Q{quarter}   Portfolio: {portfolio}   Character: {character_name}",
        True,
        WHITE,
    )
    surface.blit(label, (20, VIEWPORT_HEIGHT + 10))

    # PVI big
    pvi_label = BIG_FONT.render(f"PVI {pvi:.2f}", True, tier_color)
    surface.blit(pvi_label, (20, VIEWPORT_HEIGHT + 40))
    tier_label = MED_FONT.render(tier_text, True, tier_color)
    surface.blit(tier_label, (20, VIEWPORT_HEIGHT + 90))

    # Bars
    names = ["Performance", "Capabilities", "Foundational", "Engagement"]
    colors = [BLUE, PURPLE, GOLD, GREEN]
    x_start = 360
    y_start = VIEWPORT_HEIGHT + 40
    bar_width = 200
    bar_height = 16
    gap = 32

    for i, (name, val, col) in enumerate(zip(names, stats, colors)):
        y = y_start + i * gap
        caption = SMALL_FONT.render(f"{name}: {val:.1f}/10", True, WHITE)
        surface.blit(caption, (x_start, y - 4))

        pct = max(0.0, min(1.0, val / 10.0))
        bg_rect = pygame.Rect(x_start + 220, y, bar_width, bar_height)
        fg_rect = pygame.Rect(
            x_start + 220, y, int(bar_width * pct), bar_height
        )
        pygame.draw.rect(surface, DARK_GRAY, bg_rect, border_radius=6)
        pygame.draw.rect(surface, col, fg_rect, border_radius=6)


def draw_corridor(surface, t: float):
    """Simple animated 'first‑person' corridor background."""
    surface.fill(BLACK)
    horizon = VIEWPORT_HEIGHT // 2
    for i in range(40):
        depth = i / 40.0
        width_scale = (1.0 - depth) * 0.9 + 0.1
        line_y = horizon + int(
            math.sin(t * 0.8 + depth * 10.0) * 20 * (1 - depth)
        )
        half_width = int((WIDTH * 0.45) * width_scale)
        color = interpolate_color(DARK_GRAY, BLUE, 1 - depth)
        pygame.draw.line(
            surface,
            color,
            (WIDTH // 2 - half_width, line_y),
            (WIDTH // 2 + half_width, line_y),
            2,
        )

    # Perspective "walls"
    for offset in (-1, 1):
        for i in range(10):
            depth = i / 10.0
            start_y = VIEWPORT_HEIGHT
            end_y = 0
            start_x = WIDTH // 2 + offset * int(WIDTH * 0.2 * (1 - depth))
            end_x = WIDTH // 2 + offset * int(WIDTH * 0.4 * depth)
            color = interpolate_color(BLUE, CYAN, depth)
            pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 1)


class Game:
    def __init__(self):
        self.running = True
        self.state = "MENU"  # MENU, PORTFOLIO, CHARACTER, ADVENTURE, RESULTS
        self.portfolio = "Security"
        self.character_index = 0
        self.partner_name = "ALLY PARTNER"
        self.stats = [5.0, 5.0, 5.0, 5.0]
        self.quarter = 1
        self.pvi = compute_pvi(self.stats, self.portfolio)
        self.current_scene = 0
        self.selected_option = 0
        self.time_elapsed = 0.0

    # ---------------- STATE MANAGEMENT ----------------
    def reset_run(self):
        base = CHARACTERS[self.character_index]["stats"]
        self.stats = base.copy()
        self.quarter = 1
        self.current_scene = 0
        self.selected_option = 0
        self.pvi = compute_pvi(self.stats, self.portfolio)
        self.state = "ADVENTURE"

    def update(self, dt: float):
        self.time_elapsed += dt

    # ---------------- MENU SCREENS ----------------
    def run_menu(self):
        while self.state == "MENU" and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mx, my = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]

            SCREEN.fill(BLACK)
            draw_corridor(SCREEN, pygame.time.get_ticks() / 500.0)

            overlay = pygame.Surface((WIDTH, VIEWPORT_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            SCREEN.blit(overlay, (0, 0))

            draw_text_center(
                "Cisco 360 / Path to Preferred Partner Adventure",
                TITLE_FONT,
                CYAN,
                SCREEN,
                120,
            )
            draw_text_center(
                "A first-person strategic journey through the Cisco 360 universe.",
                MED_FONT,
                WHITE,
                SCREEN,
                170,
            )

            start_rect = pygame.Rect(WIDTH // 2 - 150, 240, 300, 60)
            quit_rect = pygame.Rect(WIDTH // 2 - 150, 320, 300, 60)

            draw_button(
                "Start Adventure",
                start_rect,
                start_rect.collidepoint(mx, my),
                SCREEN,
                PURPLE,
                CYAN,
            )
            draw_button(
                "Quit",
                quit_rect,
                quit_rect.collidepoint(mx, my),
                SCREEN,
                RED,
                (255, 60, 60),
            )

            draw_dashboard(
                SCREEN,
                self.stats,
                self.portfolio,
                self.quarter,
                self.pvi,
                CHARACTERS[self.character_index]["name"],
            )

            if click:
                if start_rect.collidepoint(mx, my):
                    self.state = "PORTFOLIO"
                elif quit_rect.collidepoint(mx, my):
                    self.running = False

            pygame.display.flip()
            CLOCK.tick(FPS)

    def run_portfolio_select(self):
        portfolios = list(PORTFOLIO_WEIGHTS.keys())
        selected = portfolios.index(self.portfolio)

        while self.state == "PORTFOLIO" and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        selected = (selected + 1) % len(portfolios)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        selected = (selected - 1) % len(portfolios)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.portfolio = portfolios[selected]
                        self.state = "CHARACTER"

            SCREEN.fill(DARK_GRAY)
            draw_corridor(SCREEN, pygame.time.get_ticks() / 600.0)

            overlay = pygame.Surface((WIDTH, VIEWPORT_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            SCREEN.blit(overlay, (0, 0))

            draw_text_center(
                "Choose Your Cisco 360 Portfolio", TITLE_FONT, CYAN, SCREEN, 120
            )
            draw_text_center(
                "Use ← → and press ENTER to confirm",
                SMALL_FONT,
                WHITE,
                SCREEN,
                160,
            )

            for i, name in enumerate(portfolios):
                color = GOLD if i == selected else WHITE
                y = 230 + i * 50
                draw_text_center(name, BIG_FONT, color, SCREEN, y)

            hint_text = (
                "Security: Capabilities weighted 45%, Foundational 30%."
                if portfolios[selected] == "Security"
                else "Networking: Balanced weighting across all motions."
            )
            draw_text_center(hint_text, SMALL_FONT, WHITE, SCREEN, 360)

            draw_dashboard(
                SCREEN,
                self.stats,
                portfolios[selected],
                self.quarter,
                compute_pvi(self.stats, portfolios[selected]),
                CHARACTERS[self.character_index]["name"],
            )

            pygame.display.flip()
            CLOCK.tick(FPS)

    def run_character_select(self):
        selected = self.character_index
        input_active = False
        name_buffer = self.partner_name

        while self.state == "CHARACTER" and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        selected = (selected + 1) % len(CHARACTERS)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        selected = (selected - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_TAB:
                        input_active = not input_active
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.character_index = selected
                        self.partner_name = name_buffer or "ALLY PARTNER"
                        self.reset_run()
                        return
                    elif input_active:
                        if event.key == pygame.K_BACKSPACE:
                            name_buffer = name_buffer[:-1]
                        else:
                            if len(name_buffer) < 22 and event.unicode.isprintable():
                                name_buffer += event.unicode.upper()

            SCREEN.fill(DARK_GRAY)
            draw_corridor(SCREEN, pygame.time.get_ticks() / 650.0)

            overlay = pygame.Surface((WIDTH, VIEWPORT_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 210))
            SCREEN.blit(overlay, (0, 0))

            draw_text_center(
                "Choose Your Base Partner Character", TITLE_FONT, CYAN, SCREEN, 90
            )
            draw_text_center(
                "Use ← → to cycle, TAB to edit name, ENTER to launch",
                SMALL_FONT,
                WHITE,
                SCREEN,
                130,
            )

            char = CHARACTERS[selected]
            draw_text_center(char["name"], BIG_FONT, GOLD, SCREEN, 190)

            desc_lines = [
                char["archetype"],
                "Represents a BASE partner entering Cisco 360.",
            ]
            for i, line in enumerate(desc_lines):
                draw_text_center(line, SMALL_FONT, WHITE, SCREEN, 230 + i * 24)

            # Firm name input
            box_rect = pygame.Rect(WIDTH // 2 - 260, 290, 520, 46)
            pygame.draw.rect(SCREEN, GRAY, box_rect, border_radius=8)
            pygame.draw.rect(
                SCREEN,
                CYAN if input_active else WHITE,
                box_rect,
                2,
                border_radius=8,
            )
            label = SMALL_FONT.render("Firm Name:", True, WHITE)
            SCREEN.blit(label, (box_rect.x + 10, box_rect.y - 24))
            name_surf = MED_FONT.render(
                name_buffer or "ALLY PARTNER", True, WHITE
            )
            SCREEN.blit(name_surf, (box_rect.x + 12, box_rect.y + 10))

            base_stats = char["stats"]
            preview_pvi = compute_pvi(base_stats, self.portfolio)

            draw_dashboard(
                SCREEN,
                base_stats,
                self.portfolio,
                1,
                preview_pvi,
                char["name"],
            )

            pygame.display.flip()
            CLOCK.tick(FPS)

    # ---------------- ADVENTURE ----------------
    def run_adventure(self):
        while self.state == "ADVENTURE" and self.running:
            dt = CLOCK.tick(FPS) / 1000.0
            self.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected_option = (self.selected_option - 1) % 2
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected_option = (self.selected_option + 1) % 2
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.apply_choice()
                        # If we've completed all scenarios, break to transition to RESULTS
                        if self.current_scene >= len(SCENARIOS):
                            break

            # Check if we've completed all scenarios before rendering
            if self.current_scene >= len(SCENARIOS):
                break

            SCREEN.fill(BLACK)
            draw_corridor(SCREEN, self.time_elapsed * 1.2)

            overlay = pygame.Surface((WIDTH, VIEWPORT_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            SCREEN.blit(overlay, (0, 0))

            scenario = SCENARIOS[self.current_scene]
            draw_text_center(scenario["title"], BIG_FONT, CYAN, SCREEN, 70)

            # Wrapped scenario text
            self.draw_wrapped_text(
                scenario["text"],
                SMALL_FONT,
                WHITE,
                (80, 110, WIDTH - 160, 120),
            )

            for i, (text, _, impact_desc) in enumerate(scenario["options"]):
                y = 250 + i * 60
                color = GOLD if i == self.selected_option else WHITE
                option_text = f"[{i+1}] {text}"
                draw_text_center(option_text, MED_FONT, color, SCREEN, y)
                sub = SMALL_FONT.render(
                    impact_desc,
                    True,
                    GREEN if i == self.selected_option else (180, 220, 180),
                )
                sub_rect = sub.get_rect(center=(WIDTH // 2, y + 26))
                SCREEN.blit(sub, sub_rect)

            draw_text_center(
                "Use ↑/↓ to choose, ENTER to commit. This is your first-person decision path.",
                SMALL_FONT,
                WHITE,
                SCREEN,
                VIEWPORT_HEIGHT - 40,
            )

            self.pvi = compute_pvi(self.stats, self.portfolio)
            draw_dashboard(
                SCREEN,
                self.stats,
                self.portfolio,
                self.quarter,
                self.pvi,
                CHARACTERS[self.character_index]["name"],
            )

            pygame.display.flip()

    def draw_wrapped_text(self, text, font, color, rect_tuple):
        rect = pygame.Rect(rect_tuple)
        words = text.split(" ")
        line = ""
        y = rect.top

        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= rect.width:
                line = test_line
            else:
                surf = font.render(line, True, color)
                SCREEN.blit(surf, (rect.left, y))
                y += font.get_linesize()
                line = word + " "
        if line:
            surf = font.render(line, True, color)
            SCREEN.blit(surf, (rect.left, y))

    def apply_choice(self):
        scenario = SCENARIOS[self.current_scene]
        _, deltas, _ = scenario["options"][self.selected_option]
        for i in range(4):
            self.stats[i] += deltas[i]
        self.quarter += 1
        self.current_scene += 1

        if self.current_scene >= len(SCENARIOS):
            self.state = "RESULTS"

    # ---------------- RESULTS / LOOP BACK ----------------
    def run_results(self):
        final_pvi = compute_pvi(self.stats, self.portfolio)
        tier_text, tier_color = pvi_tier(final_pvi)
        decision = "MENU"  # or "QUIT"

        while self.state == "RESULTS" and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "MENU" if decision == "MENU" else "QUIT"
                        if self.state == "QUIT":
                            self.running = False
                        return
                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_a,
                        pygame.K_RIGHT,
                        pygame.K_d,
                    ):
                        decision = "MENU" if decision == "QUIT" else "QUIT"

            SCREEN.fill(DARK_GRAY)
            draw_corridor(SCREEN, pygame.time.get_ticks() / 700.0)
            overlay = pygame.Surface((WIDTH, VIEWPORT_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))
            SCREEN.blit(overlay, (0, 0))

            draw_text_center(
                "FISCAL YEAR SUMMARY", TITLE_FONT, CYAN, SCREEN, 90
            )

            draw_text_center(
                f"Partner: {self.partner_name}  |  Portfolio: {self.portfolio}",
                SMALL_FONT,
                WHITE,
                SCREEN,
                140,
            )

            pvi_label = BIG_FONT.render(
                f"Final PVI: {final_pvi:.2f}", True, tier_color
            )
            SCREEN.blit(pvi_label, (WIDTH // 2 - 200, 180))
            tier_label = MED_FONT.render(tier_text, True, tier_color)
            SCREEN.blit(tier_label, (WIDTH // 2 - 200, 230))

            benefit_lines = []
            if final_pvi >= 7.5:
                benefit_lines = [
                    "You are a Cisco Preferred Partner.",
                    "Maximum rebates, Next-Gen Specializations, and 10 Cisco U licenses unlocked.",
                ]
            elif final_pvi >= 5.0:
                benefit_lines = [
                    "You are a Cisco Portfolio Partner.",
                    "Base rebates and customer assessment incentives are unlocked.",
                ]
            else:
                benefit_lines = [
                    "You remain a Base Partner.",
                    "Grow Capabilities and Foundational maturity to unlock more value.",
                ]

            for i, line in enumerate(benefit_lines):
                draw_text_center(
                    line, SMALL_FONT, WHITE, SCREEN, 280 + i * 24
                )

            # Menu vs Quit options
            menu_color = GOLD if decision == "MENU" else WHITE
            quit_color = GOLD if decision == "QUIT" else WHITE
            draw_text_center(
                "Press ENTER to confirm choice",
                SMALL_FONT,
                WHITE,
                SCREEN,
                360,
            )
            draw_text_center(
                "[←/→] Return to Main Menu",
                MED_FONT,
                menu_color,
                SCREEN,
                400,
            )
            draw_text_center(
                "[←/→] Exit Game", MED_FONT, quit_color, SCREEN, 440
            )

            draw_dashboard(
                SCREEN,
                self.stats,
                self.portfolio,
                self.quarter - 1,
                final_pvi,
                CHARACTERS[self.character_index]["name"],
            )

            pygame.display.flip()
            CLOCK.tick(FPS)

    # ---------------- MAIN LOOP ----------------
    def run(self):
        while self.running:
            if self.state == "MENU":
                self.run_menu()
            elif self.state == "PORTFOLIO":
                self.run_portfolio_select()
            elif self.state == "CHARACTER":
                self.run_character_select()
            elif self.state == "ADVENTURE":
                self.run_adventure()
            elif self.state == "RESULTS":
                self.run_results()
            else:
                self.running = False

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.display.set_caption(
        "Cisco 360 / Path to Preferred Partner Adventure"
    )
    Game().run()
