import os
import string
import random
import pygame
import numpy as np

from config import (
    CELL_SIZE, STEP_DELAY_MIN, STEP_DELAY_MAX, TRAINING_EPISODES, MODEL_SAVE_INTERVAL,
    BLACK, GREEN, RED, BLUE, YELLOW
)

class SnakeGame:
    def __init__(self, game_id, agent, x, y, cell_size=CELL_SIZE, grid_size=20):
        self.game_id = game_id
        self.agent = agent
        self.eating = False
        self.x = x  # Top-left x coordinate of the game cell.
        self.y = y  # Top-left y coordinate.
        self.cell_size = cell_size
        self.grid_size = grid_size  # The game grid is grid_size x grid_size.
        self.cell_pixel = cell_size // grid_size  # Pixel size of each grid cell.
        self.reset()
        self.running = False
        self.game_over = False
        self.last_update_time = pygame.time.get_ticks()
        self.step_delay = 200  # Default delay in ms.
    
    def reset(self):
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self):
        while True:
            self.food = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1)
            )
            if self.food not in self.snake:
                break

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time < self.step_delay:
            return
        self.last_update_time = current_time
        
        features = self.extract_features()
        action = self.agent.decide_move(features)
        self.update_direction(action)
        
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )
        
        reward = -0.01  # Time-step penalty.
        self.eating = False
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake):
            reward = -1.0
            self.game_over = True
            done = True
        else:
            done = False
            self.snake.insert(0, new_head)
            if new_head == self.food:
                reward = 1.0
                self.score += 1
                self.place_food()
                self.eating = True
            else:
                self.snake.pop()
        
        next_features = self.extract_features()
        
        if self.agent.mode == 'training':
            loss = self.agent.learn(features, action, reward, next_features, done)
        
        if self.game_over:
            if self.agent.mode == 'training':
                self.agent.training_episode += 1
                if self.agent.training_episode % MODEL_SAVE_INTERVAL == 0:
                    # Define the folder path and ensure it exists.
                    folder_path = f"models/{self.game_id}/{self.agent.training_episode}"
                    os.makedirs(folder_path, exist_ok=True)
                    # Define the filename using the folder path.
                    filename = f"{folder_path}/snake_model_score_{self.score}_{self.generate_random_string()}.pth"
                    self.agent.save_model(filename)
                    print(f"Saved model at episode {self.agent.training_episode} | Score: {self.score} | Epsilon: {self.agent.epsilon:.3f}")
                if self.agent.training_episode >= TRAINING_EPISODES:
                    self.running = False
                    print("Training complete!")
                    return
                self.reset()
            else:
                self.running = False

    def generate_random_string(self, length=8):
        characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
        print(characters)
        return ''.join(random.choices(characters, k=length))
    
    def update_direction(self, action):
        dx, dy = self.direction
        if action == 1:  # Right turn.
            self.direction = (dy, -dx)
        elif action == 2:  # Left turn.
            self.direction = (-dy, dx)
        # Action 0: continue straight.

    def extract_features(self):
        """Extract 7 normalized features:
           - 3 collision distances (straight, right, left)
           - 3 food distances (straight, right, left)
           - 1 normalized score feature.
        """
        features = []
        dx, dy = self.direction
        directions = [
            self.direction,           # straight
            (dy, -dx),                # right turn
            (-dy, dx)                 # left turn
        ]
        for d in directions:
            features.append(self.distance_to_collision(d))
        for d in directions:
            features.append(self.distance_to_food(d))
        features.append(self.score / 10.0)
        return np.array(features)

    def distance_to_collision(self, d):
        head = self.snake[0]
        distance = 0
        x, y = head
        while True:
            x += d[0]
            y += d[1]
            distance += 1
            if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
                break
            if (x, y) in self.snake:
                break
        return distance / self.grid_size

    def distance_to_food(self, d):
        head = self.snake[0]
        fx, fy = self.food
        dx, dy = d
        if dx != 0 and (fx - head[0]) * dx > 0:
            return abs(fx - head[0]) / self.grid_size
        if dy != 0 and (fy - head[1]) * dy > 0:
            return abs(fy - head[1]) / self.grid_size
        return 1.0

    def render(self, surface):
        rect = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
        color = BLACK if not self.eating else GREEN
        color = color if not self.game_over else RED
        pygame.draw.rect(surface, color, rect)
        
        for i in range(self.grid_size + 1):
            pygame.draw.line(surface, BLACK, (self.x, self.y + i * self.cell_pixel),
                             (self.x + self.cell_size, self.y + i * self.cell_pixel))
            pygame.draw.line(surface, BLACK, (self.x + i * self.cell_pixel, self.y),
                             (self.x + i * self.cell_pixel, self.y + self.cell_size))
        
        for segment in self.snake:
            seg_rect = pygame.Rect(
                self.x + segment[0] * self.cell_pixel,
                self.y + segment[1] * self.cell_pixel,
                self.cell_pixel,
                self.cell_pixel
            )
            pygame.draw.rect(surface, BLUE, seg_rect)
        
        food_rect = pygame.Rect(
            self.x + self.food[0] * self.cell_pixel,
            self.y + self.food[1] * self.cell_pixel,
            self.cell_pixel,
            self.cell_pixel
        )
        pygame.draw.rect(surface, YELLOW, food_rect)
        
        font = pygame.font.SysFont("Arial", 16)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (self.x + 5, self.y + self.cell_size - 20))

    def set_step_delay(self, delay):
        self.step_delay = max(STEP_DELAY_MIN, min(delay, STEP_DELAY_MAX))
