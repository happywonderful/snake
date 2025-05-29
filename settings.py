# 游戏配置参数

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色设置 (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 游戏设置
INITIAL_SNAKE_LENGTH = 3
INITIAL_SPEED = 2  # 初始速度
SPEED_INCREMENT = 2  # 每关速度增加值
MAX_LEVEL = 3  # 最大关卡数

# 每关的障碍物数量
OBSTACLES_PER_LEVEL = {
    1: 0,    # 第1关没有障碍物
    2: 3,    # 第2关3个障碍物
    3: 5,
    4: 7,
    5: 10,
    6: 13,
    7: 16,
    8: 20,
    9: 25,
    10: 30   # 最后一关30个障碍物
}

# 方向键设置
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

# 游戏状态
GAME_RUNNING = 'RUNNING'
GAME_PAUSED = 'PAUSED'
GAME_OVER = 'GAME_OVER'
LEVEL_COMPLETE = 'LEVEL_COMPLETE'
GAME_WIN = 'GAME_WIN'

# 分数设置
FOOD_SCORE = 10  # 每个食物的分数
LEVEL_COMPLETE_BONUS = 30  # 完成关卡奖励分数