import pygame
from config import GRAY, WHITE, BLACK, GREEN, RED, BLUE, STEP_DELAY_MIN, STEP_DELAY_MAX

class ControlPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 20)
        self.start_button = pygame.Rect(x + 10, y + 10, 80, 30)
        self.pause_button = pygame.Rect(x + 100, y + 10, 80, 30)
        self.mode_toggle = pygame.Rect(x + 190, y + 10, 150, 30)
        self.step_delay_slider = pygame.Rect(x + 350, y + 10, 200, 30)
        self.mode = 'training'
        self.step_delay = 200
        self.buttons_enabled = True

    def render(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, GREEN if self.buttons_enabled else (150, 150, 150), self.start_button)
        start_text = self.font.render("Start", True, BLACK)
        surface.blit(start_text, (self.start_button.x + 10, self.start_button.y + 5))
        pygame.draw.rect(surface, RED if self.buttons_enabled else (150, 150, 150), self.pause_button)
        pause_text = self.font.render("Pause", True, BLACK)
        surface.blit(pause_text, (self.pause_button.x + 10, self.pause_button.y + 5))
        pygame.draw.rect(surface, WHITE if self.buttons_enabled else (200, 200, 200), self.mode_toggle)
        mode_text = self.font.render(f"Mode: {self.mode}", True, BLACK)
        surface.blit(mode_text, (self.mode_toggle.x + 10, self.mode_toggle.y + 5))
        pygame.draw.rect(surface, WHITE if self.buttons_enabled else (200, 200, 200), self.step_delay_slider)
        delay_text = self.font.render(f"Delay: {self.step_delay}ms", True, BLACK)
        surface.blit(delay_text, (self.step_delay_slider.x + 10, self.step_delay_slider.y + 5))

    def handle_event(self, event):
        if not self.buttons_enabled:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.start_button.collidepoint(pos):
                return "start"
            elif self.pause_button.collidepoint(pos):
                return "pause"
            elif self.mode_toggle.collidepoint(pos):
                self.mode = 'inference' if self.mode == 'training' else 'training'
                return "mode_toggle"
            elif self.step_delay_slider.collidepoint(pos):
                if self.step_delay < STEP_DELAY_MAX:
                    self.step_delay += 50
                else:
                    self.step_delay = STEP_DELAY_MIN
                return "step_delay"
        return None

    def disable_buttons(self):
        self.buttons_enabled = False

    def enable_buttons(self):
        self.buttons_enabled = True
