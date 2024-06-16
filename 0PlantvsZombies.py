# main.py
import pygame
import sys
from sun import Sun 
#import zombie  
import menu  
from slots import draw_slots  
#import sunflower
import color

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption('Plants vs Zombies')

# 调用主界面函数
menu.main_menu(screen)

# 创建Sun对象
sun = Sun(screen_width, screen_height)

# 创建Sunflower对象
#sunflower = Sunflower(screen_width, screen_height)

# 创建Zombie对象
#zombie_manager = zombie.Zombie(screen_width, screen_height)

# 设置游戏时钟
clock = pygame.time.Clock()

# 初始化字体
pygame.font.init()
font = pygame.font.SysFont(None, 36)



# 游戏主循环
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        sun.handle_events(event)  # 识别鼠标点击
        #zombie_manager.handle_events(event)  # 识别鼠标点击

    # 填充背景色
    screen.fill(color.lightgreen)

    # 绘制卡槽
    draw_slots(screen)

    # 更新并绘制阳光
    sun.update(screen)

    # 生成并更新僵尸
    #zombie_manager.generate_zombies()
    #zombie_manager.update_zombies(screen)

    # 绘制击杀数目
    #zombie_manager.draw_kill_count(screen)

    # 更新屏幕
    pygame.display.flip()

    # 控制游戏速度
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()