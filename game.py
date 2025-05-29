import pygame
import random
from settings import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        # 初始化游戏状态
        self.game_state = GAME_RUNNING
        self.level = 1
        self.score = 0
        self.speed = INITIAL_SPEED
        
        # 初始化蛇的位置和方向
        self.snake_positions = [
            (GRID_WIDTH // 4, GRID_HEIGHT // 2),
            (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 4 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = RIGHT
        
        # 生成食物和障碍物
        self.generate_food()
        self.generate_obstacles()

    def generate_food(self):
        while True:
            self.food_position = (random.randint(0, GRID_WIDTH - 1),
                                random.randint(0, GRID_HEIGHT - 1))
            if (self.food_position not in self.snake_positions and
                self.food_position not in self.obstacles):
                break

    def generate_obstacles(self):
        self.obstacles = set()
        num_obstacles = OBSTACLES_PER_LEVEL.get(self.level, 0)
        
        for _ in range(num_obstacles):
            while True:
                obstacle = (random.randint(0, GRID_WIDTH - 1),
                          random.randint(0, GRID_HEIGHT - 1))
                if (obstacle not in self.snake_positions and
                    obstacle not in self.obstacles and
                    obstacle != self.food_position):
                    self.obstacles.add(obstacle)
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.game_state == GAME_RUNNING:
                        self.game_state = GAME_PAUSED
                    elif self.game_state == GAME_PAUSED:
                        self.game_state = GAME_RUNNING
                        
                if event.key == pygame.K_r:
                    if self.game_state in [GAME_OVER, GAME_WIN]:
                        self.reset_game()
                        
                if self.game_state == GAME_RUNNING:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.direction = RIGHT

    def update(self):
        if self.game_state != GAME_RUNNING:
            return
            
        # 移动蛇
        head_x, head_y = self.snake_positions[0]
        if self.direction == UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == LEFT:
            new_head = (head_x - 1, head_y)
        else:  # RIGHT
            new_head = (head_x + 1, head_y)
            
        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake_positions or
            new_head in self.obstacles):
            self.game_state = GAME_OVER
            return
            
        # 移动蛇
        self.snake_positions.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.food_position:
            self.score += FOOD_SCORE
            self.generate_food()
            
            # 检查是否完成当前关卡
            if len(self.snake_positions) >= INITIAL_SNAKE_LENGTH + self.level * 5:
                if self.level >= MAX_LEVEL:
                    self.game_state = GAME_WIN
                else:
                    self.level += 1
                    self.speed += SPEED_INCREMENT
                    self.score += LEVEL_COMPLETE_BONUS
                    self.game_state = LEVEL_COMPLETE
                    self.generate_obstacles()
        else:
            self.snake_positions.pop()
            
        # 控制游戏速度
        self.clock.tick(self.speed * 5)

    def draw(self):
        # 清空屏幕
        self.screen.fill(BLACK)
        
        # 绘制网格
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE,
                                 GRID_SIZE - 1, GRID_SIZE - 1)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
        
        # 绘制蛇
        for segment in self.snake_positions:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                             GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(self.screen, GREEN, rect)
            
        # 绘制食物
        food_rect = pygame.Rect(self.food_position[0] * GRID_SIZE,
                               self.food_position[1] * GRID_SIZE,
                               GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 绘制障碍物
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle[0] * GRID_SIZE,
                                      obstacle[1] * GRID_SIZE,
                                      GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(self.screen, BLUE, obstacle_rect)
        
        # 绘制得分和关卡信息
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        
        # 绘制游戏状态信息
        if self.game_state == GAME_PAUSED:
            self.draw_message('游戏暂停 - 按P继续')
        elif self.game_state == GAME_OVER:
            self.draw_message('游戏结束 - 按R重新开始')
        elif self.game_state == LEVEL_COMPLETE:
            self.draw_message(f'第{self.level-1}关完成！按任意键继续...')
        elif self.game_state == GAME_WIN:
            self.draw_message('恭喜通关！按R重新开始')

    def draw_message(self, message):
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(text, text_rect)