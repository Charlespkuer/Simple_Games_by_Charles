# sunflower.py
import pygame

class sunflower:
    def __init__(self, screen):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.plant_slot_width = 70
        self.plant_slot_height = 70
        self.plant_slot_spacing = 10
        self.plant_slot_count = 5
        self.start_x = (self.screen_width - (self.plant_slot_count * self.plant_slot_width + (self.plant_slot_count - 1) * self.plant_slot_spacing)) // 2

    def draw_sunflower(self, screen, colors, position_x, position_y):
        slot_x = self.start_x + position_x
        # 绘制太阳花的花瓣
        pygame.draw.ellipse(screen, colors["YELLOW"], (slot_x + 13, 7, self.plant_slot_width - 26, self.plant_slot_height - 24))
        # 绘制太阳花的花蕊
        pygame.draw.ellipse(screen, colors["BROWN"], (slot_x + 20, 15, self.plant_slot_width - 40, self.plant_slot_height - 40))
        # 绘制笑脸
        center_x = slot_x + self.plant_slot_width // 2
        center_y = self.plant_slot_height // 2 + 10
        radius = (self.plant_slot_width - 40) // 2
        pygame.draw.circle(screen, colors["YELLOW"], (center_x - radius // 3, center_y - radius - 10 // 3), radius // 8)  # 左眼
        pygame.draw.circle(screen, colors["YELLOW"], (center_x + radius // 3, center_y - radius - 10 // 3), radius // 8)  # 右眼
        pygame.draw.arc(screen, colors["YELLOW"], (center_x - radius // 2, center_y - radius - 10 // 2, radius, radius), 3.14, 0, 1)  # 微笑的弧线
        # 绘制茎和叶子
        pygame.draw.rect(screen, colors["GREEN"], (slot_x + 31, self.plant_slot_height - 18, 7, 20))  # 茎
        pygame.draw.polygon(screen, colors["GREEN"], [(slot_x + 15, self.plant_slot_height - 10), (slot_x + 35, self.plant_slot_height - 10), (slot_x + 35, self.plant_slot_height)])  # 叶子
        pygame.draw.polygon(screen, colors["GREEN"], [(slot_x + 52, self.plant_slot_height - 10), (slot_x + 36, self.plant_slot_height - 10), (slot_x + 36, self.plant_slot_height - 1)])  # 叶子