import pygame


class TextBox:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

        self.text = ""
        self.active = True

        self.color_active = (70, 140, 240)
        self.color_inactive = (120, 120, 130)

        self.font = pygame.font.SysFont(None, 36)

    def handle_event(self, event):

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        # Keyboard input
        elif event.type == pygame.KEYDOWN and self.active:

            # Backspace
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            # Numbers only
            elif event.unicode.isdigit() and len(self.text) < 3:
                self.text += event.unicode

    def clear(self):
        self.text = ""

    def render(self, surface):

        # Choose border color based on focus
        box_color = (
            self.color_active
            if self.active
            else self.color_inactive
        )

        # White background
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            self.rect,
            border_radius=6
        )

        # Colored border
        pygame.draw.rect(
            surface,
            box_color,
            self.rect,
            width=3,
            border_radius=6
        )

        # Render entered text
        text_surf = self.font.render(
            self.text,
            True,
            (20, 20, 20)
        )

        surface.blit(
            text_surf,
            (
                self.rect.x + 15,
                self.rect.y + 10
            )
        )