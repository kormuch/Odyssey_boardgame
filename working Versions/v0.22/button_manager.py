# button_manager.py
import pygame
from gamelog import logger  # import the session logger


class ButtonManager:
    """Manages button layouts and interactions"""

    def __init__(self, screen_width, screen_height):
        self.WIDTH = screen_width
        self.HEIGHT = screen_height
        self.button_height = 50
        self.button_margin_bottom = 10
        self.button_start_y = self.HEIGHT - self.button_height - self.button_margin_bottom
        self.button_width = self.WIDTH // 4
        self.small_button_width = 120

        # Button definitions
        self.action_buttons = ["Battle", "Wits", "Fellowship", "Journey"]
        self.control_buttons = ["Next Player", "Skip Turn", "Show Cards", "New Level"]

        # Calculate positions for special buttons
        self.quit_button_rect = pygame.Rect(
            self.WIDTH - 80 - 10,
            10,
            80,
            30
        )
        self.start_button_rect = pygame.Rect(
            self.WIDTH // 2 - self.button_width // 2,
            400,
            self.button_width,
            self.button_height
        )

    def get_action_button_rect(self, index):
        if 0 <= index < len(self.action_buttons):
            rect = pygame.Rect(
                index * self.button_width,
                self.button_start_y,
                self.button_width,
                self.button_height
            )
            return rect
        return None

    def get_control_button_rect(self, index):
        if 0 <= index < len(self.control_buttons):
            rect = pygame.Rect(
                20,
                20 + index * (self.button_height + 5),
                self.small_button_width,
                self.button_height
            )
            return rect
        return None

    def get_clicked_button(self, pos):
        for i, button_name in enumerate(self.action_buttons):
            button_rect = self.get_action_button_rect(i)
            if button_rect and button_rect.collidepoint(pos):
                return ("action", button_name)

        for i, button_name in enumerate(self.control_buttons):
            button_rect = self.get_control_button_rect(i)
            if button_rect and button_rect.collidepoint(pos):
                return ("control", button_name)

        if self.quit_button_rect.collidepoint(pos):
            return ("special", "quit")
        if self.start_button_rect.collidepoint(pos):
            return ("special", "start")

        return None

    def add_action_button(self, button_name):
        if button_name not in self.action_buttons:
            self.action_buttons.append(button_name)
            self.button_width = self.WIDTH // len(self.action_buttons)
        else:
            pass  # nothing to do, previously logged

    def add_control_button(self, button_name):
        if button_name not in self.control_buttons:
            self.control_buttons.append(button_name)
        else:
            pass  # nothing to do, previously logged

    def remove_action_button(self, button_name):
        if button_name in self.action_buttons:
            self.action_buttons.remove(button_name)
            if self.action_buttons:
                self.button_width = self.WIDTH // len(self.action_buttons)
        else:
            pass  # nothing to do, previously logged

    def remove_control_button(self, button_name):
        if button_name in self.control_buttons:
            self.control_buttons.remove(button_name)
        else:
            pass  # nothing to do, previously logged

    def get_all_button_rects(self):
        rects = {}
        for i, name in enumerate(self.action_buttons):
            rects[f"action_{name}"] = self.get_action_button_rect(i)
        for i, name in enumerate(self.control_buttons):
            rects[f"control_{name}"] = self.get_control_button_rect(i)
        rects["quit"] = self.quit_button_rect
        rects["start"] = self.start_button_rect
        return rects

    def is_point_on_any_button(self, pos):
        result = self.get_clicked_button(pos) is not None
        return result
