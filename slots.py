# slots.py
import pygame
from sun import Sun  # 导入Sun类

# 卡槽的参数
plant_slot_width = 70
plant_slot_height = 70
plant_slot_spacing = 10
plant_slot_count = 6

DARK_GREEN = (0, 100, 0)

def draw_slots(screen):

    # 创建Sun对象
    sun = Sun(screen.get_width(), screen.get_height())
    # 绘制卡槽
    total_plant_slot_width = plant_slot_count * plant_slot_width + (plant_slot_count - 1) * plant_slot_spacing
    start_x = (screen.get_width() - total_plant_slot_width) // 2
    for i in range(plant_slot_count):
        slot_x = start_x + i * (plant_slot_width + plant_slot_spacing)
        pygame.draw.rect(screen, DARK_GREEN, (slot_x, 0, plant_slot_width, plant_slot_height))

    # 绘制太阳卡槽
    pygame.draw.rect(screen, DARK_GREEN, (15, 0, plant_slot_width, plant_slot_height))
    sun_position = (15 + plant_slot_width // 2, plant_slot_height // 2)
    sun.draw_sun(screen, sun_position)