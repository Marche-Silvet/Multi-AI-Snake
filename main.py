# main.py

import sys
import random
import pygame
import tkinter as tk
from tkinter import filedialog

from config import *
from agent.snake_agent import SnakeAgent
from game.snake_game import SnakeGame
from ui.control_panel import ControlPanel

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Multi-Instance Snake Game with Training")
    clock = pygame.time.Clock()

    # Create the control panel at the bottom.
    control_panel = ControlPanel(
        0, 
        WINDOW_HEIGHT - CONTROL_PANEL_HEIGHT + GRID_Y_OFFSET, 
        WINDOW_WIDTH, 
        CONTROL_PANEL_HEIGHT
    )

    # Dictionary for game instances on grid cells.
    instances = {}
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            instances[(row, col)] = None

    global_running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            action = control_panel.handle_event(event)
            if action == "start":
                global_running = True
                control_panel.disable_buttons()
                for inst in instances.values():
                    if inst is not None:
                        inst.running = True
            elif action == "pause":
                global_running = False
                control_panel.enable_buttons()
                for inst in instances.values():
                    if inst is not None:
                        inst.running = False
            elif action == "mode_toggle":
                for inst in instances.values():
                    if inst is not None:
                        inst.agent.set_mode(control_panel.mode)
            elif action == "step_delay":
                for inst in instances.values():
                    if inst is not None:
                        inst.set_step_delay(control_panel.step_delay)

            # Handle mouse clicks in the grid area.
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < WINDOW_HEIGHT - CONTROL_PANEL_HEIGHT:
                    for (row, col), game_instance in instances.items():
                        cell_x = GRID_X_OFFSET + col * (CELL_SIZE + CELL_PADDING)
                        cell_y = GRID_Y_OFFSET + row * (CELL_SIZE + CELL_PADDING)
                        cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                        if cell_rect.collidepoint(pos):
                            if game_instance is not None:
                                # Define load and delete button areas.
                                load_rect = pygame.Rect(cell_x, cell_y, 20, 20)
                                delete_rect = pygame.Rect(cell_x + CELL_SIZE - 20, cell_y, 20, 20)
                                if control_panel.mode == 'inference' and load_rect.collidepoint(pos):
                                    root = tk.Tk()
                                    root.withdraw()
                                    filename = filedialog.askopenfilename(filetypes=[("PyTorch Model", "*.pth")])
                                    root.destroy()
                                    if filename:
                                        game_instance.agent.load_model(filename)
                                    continue
                                if delete_rect.collidepoint(pos):
                                    instances[(row, col)] = None
                            else:
                                # Create a new game instance.
                                agent = SnakeAgent(mode=control_panel.mode)
                                new_game = SnakeGame(f"game_{row}_{col}", agent, cell_x, cell_y)
                                instances[(row, col)] = new_game

        # Rendering the grid and control panel.
        screen.fill(WHITE)
        for (row, col), game_instance in instances.items():
            cell_x = GRID_X_OFFSET + col * (CELL_SIZE + CELL_PADDING)
            cell_y = GRID_Y_OFFSET + row * (CELL_SIZE + CELL_PADDING)
            cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            if game_instance is None:
                pygame.draw.rect(screen, GRAY, cell_rect)
                font = pygame.font.SysFont("Arial", 24)
                text = font.render("Add Game", True, BLACK)
                text_rect = text.get_rect(center=cell_rect.center)
                screen.blit(text, text_rect)
            else:
                if game_instance.running:
                    game_instance.update()
                game_instance.render(screen)
                if cell_rect.collidepoint(pygame.mouse.get_pos()):
                    delete_rect = pygame.Rect(cell_x + CELL_SIZE - 20, cell_y, 20, 20)
                    pygame.draw.rect(screen, RED, delete_rect)
                    font = pygame.font.SysFont("Arial", 16)
                    x_text = font.render("x", True, WHITE)
                    screen.blit(x_text, (delete_rect.x + 5, delete_rect.y))
                    if control_panel.mode == 'inference':
                        load_rect = pygame.Rect(cell_x, cell_y, 20, 20)
                        pygame.draw.rect(screen, BLUE, load_rect)
                        load_text = font.render("L", True, WHITE)
                        screen.blit(load_text, (load_rect.x + 3, load_rect.y))
        control_panel.render(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
