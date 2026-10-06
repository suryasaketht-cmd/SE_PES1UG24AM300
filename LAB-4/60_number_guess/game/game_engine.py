import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.max_attempts = 10
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        self.min_value = 1
        self.max_value = 100

        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False
        self.game_over = False

        # Input box
        self.input_box = TextBox(
            width // 2 - 110,
            150,
            120,
            48
        )

        # Submit button
        self.submit_btn = pygame.Rect(
            width // 2 + 25,
            150,
            100,
            48
        )

        # Guess history panel
        self.history_panel = pygame.Rect(
            width // 2 + 150,
            95,
            180,
            150
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 22)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        text = self.input_box.text.strip()

        if not text:
            self.feedback_msg = "Please enter a number before submitting."
            self.feedback_color = (240, 180, 60)
            return

        try:
            guess = int(text)
        except ValueError:
            self.feedback_msg = "Please enter a valid number."
            self.feedback_color = (240, 180, 60)
            return

        if guess < 1 or guess > 100:
            self.feedback_msg = "Number must be between 1 and 100."
            self.feedback_color = (240, 180, 60)
            return

        # Count valid guesses
        self.attempts += 1
        self.input_box.clear()

        # Check guess
        if guess < self.secret_number:
            self.min_value = max(self.min_value, guess + 1)

            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

            self.guess_history.append((guess, "LOW"))

        elif guess > self.secret_number:
            self.max_value = min(self.max_value, guess - 1)

            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

            self.guess_history.append((guess, "HIGH"))

        else:
            self.feedback_msg = (
                f"CORRECT! Found in {self.attempts} attempts."
            )
            self.feedback_color = (80, 220, 90)

            self.guess_history.append((guess, "CORRECT"))

            self.game_won = True

        # Keep only the latest 5 guesses
        if len(self.guess_history) > 5:
            self.guess_history = self.guess_history[-5:]

        # Check game over
        if not self.game_won and self.attempts >= self.max_attempts:
            self.game_over = True

            self.feedback_msg = (
                f"GAME OVER! The number was {self.secret_number}. "
                f"Press [R] to play again."
            )

            self.feedback_color = (255, 120, 120)

    def reset(self):
        self.secret_number = random.randint(1, 100)

        self.attempts = 0
        self.min_value = 1
        self.max_value = 100

        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False
        self.game_over = False

        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:

            # Submit with Enter
            if event.key == pygame.K_RETURN:
                self.submit_guess()

            # Restart after game ends
            elif event.key == pygame.K_r:
                if self.game_won or self.game_over:
                    self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        # Background
        screen.fill((30, 34, 42))

        # -------------------------
        # TITLE
        # -------------------------

        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                35
            )
        )

        # -------------------------
        # ATTEMPTS
        # -------------------------

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.max_attempts}",
            True,
            (180, 185, 195)
        )

        screen.blit(
            attempts_surf,
            (
                self.width // 2 - attempts_surf.get_width() // 2,
                95
            )
        )

        # -------------------------
        # RANGE
        # -------------------------

        range_surf = self.font_medium.render(
            f"Range: {self.min_value} - {self.max_value}",
            True,
            (200, 220, 255)
        )

        screen.blit(
            range_surf,
            (
                self.width // 2 - range_surf.get_width() // 2,
                125
            )
        )

        # -------------------------
        # INPUT BOX
        # -------------------------

        self.input_box.render(screen)

        # -------------------------
        # SUBMIT BUTTON
        # -------------------------

        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2
            )
        )

        # -------------------------
        # HISTORY PANEL
        # -------------------------

        pygame.draw.rect(
            screen,
            (48, 52, 63),
            self.history_panel,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (130, 140, 160),
            self.history_panel,
            width=2,
            border_radius=8
        )

        history_title = self.font_small.render(
            "Recent guesses",
            True,
            (210, 210, 220)
        )

        screen.blit(
            history_title,
            (
                self.history_panel.x + 12,
                self.history_panel.y + 10
            )
        )

        # Recent guesses
        for index, (guess, result) in enumerate(self.guess_history[-5:]):

            if result == "LOW":
                marker = "▲"
                color = (80, 160, 240)

            elif result == "HIGH":
                marker = "▼"
                color = (240, 100, 80)

            else:
                marker = "✓"
                color = (80, 220, 90)

            line = self.font_small.render(
                f"{marker} {guess}",
                True,
                color
            )

            screen.blit(
                line,
                (
                    self.history_panel.x + 14,
                    self.history_panel.y + 38 + index * 22
                )
            )

        # -------------------------
        # FEEDBACK
        # -------------------------

        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                235
            )
        )

        # -------------------------
        # RESTART MESSAGE
        # -------------------------

        if self.game_won or self.game_over:

            restart_surf = self.font_medium.render(
                "Press [R] to Start a New Game",
                True,
                (255, 220, 80)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    295
                )
            )