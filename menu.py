# menu.py
import pygame
import sys
import color


pygame.init()

# 设置字体
font = pygame.font.SysFont(None, 48)

# 主界面函数
def main_menu(screen):
    while True:
        screen.fill(color.lightgreen)

        # 绘制标题
        title_text = font.render("Plants vs Zombies", True, color.black)
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
        screen.blit(title_text, title_rect)

        # 绘制按钮
        button_width, button_height = 200, 50
        start_button = pygame.Rect((screen.get_width() - button_width) / 2, screen.get_height() / 2 + 50, button_width, button_height)
        quit_button = pygame.Rect((screen.get_width() - button_width) / 2, screen.get_height() / 2 + 120, button_width, button_height)
        pygame.draw.rect(screen, color.darkgreen, start_button)
        pygame.draw.rect(screen, color.darkgreen, quit_button)

        # 绘制按钮文本
        start_text = font.render("Start Game", True, color.white)
        quit_text = font.render("Quit", True, color.white)
        start_text_rect = start_text.get_rect(center=start_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return  # 开始游戏
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # 退出游戏

        # 更新屏幕
        pygame.display.flip()