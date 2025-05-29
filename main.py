# 主程序入口

import pygame
from game import Game
from settings import *

def main():
    # 初始化Pygame
    pygame.init()
    
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('贪吃蛇游戏')
    
    # 创建游戏实例
    game = Game(screen)
    
    # 游戏主循环
    while True:
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()

if __name__ == '__main__':
    main()