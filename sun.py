import pygame
import random
import math

# 设置颜色
YELLOW = (255, 255, 0)

# 设置太阳大小和生成参数
SUN_RADIUS = 18
SUN_GENERATE_INTERVAL = 2000  # 单位毫秒
SUN_FALL_SPEED = 1.3
SUN_ROTATION_SPEED = 0.005  # 太阳旋转速度
SUN_MOVE_SPEED = 15  # 太阳移动到太阳卡槽的速度

# 设置放射状边缘的数量
NUM_RAYS = 17

    # 计算太阳移动速度的函数
def calculate_sun_move_speed(distance, max_distance):
    # 使用线性函数来计算移动速度
    # 当距离目标位置很远时，速度接近最大速度
    # 当距离目标位置很近时，速度接近最小速度
    # 最小速度是最大速度的一半
    delta_speed = SUN_MOVE_SPEED
    speed = SUN_MOVE_SPEED + delta_speed * (3*(distance-100) / max_distance)
    return speed

class Sun:#太阳类
    def __init__(self, screen_width, screen_height): # 初始化太阳的属性
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.suns = []
        self.sun_count = 50  # 初始阳光数量
        self.last_sun_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 36)  # 字体
        self.SUN_VALUE = 25
        self.rotation_angle = 0  # 太阳的初始旋转角度
        self.sun_slot_position = (50, 35)  # 太阳卡槽的位置

    def generate_suns(self):#生成太阳
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sun_time > SUN_GENERATE_INTERVAL:
            self.last_sun_time = current_time
            sun_x = random.randint(0 + 6 * SUN_RADIUS, self.screen_width - 6 * SUN_RADIUS)
            sun_y = -SUN_RADIUS
            self.suns.append({'rect': pygame.Rect(sun_x, sun_y, SUN_RADIUS * 4, SUN_RADIUS * 4), 'moving': False})
    
    def update_suns(self, screen):#每帧更新太阳
        for sun in self.suns[:]:
            if sun['moving']:
                # 太阳正在移动到太阳卡槽
                dx = sun['target_x'] - sun['rect'].centerx
                dy = sun['target_y'] - sun['rect'].centery
                distance = math.hypot(dx, dy)
                # 假设屏幕对角线长度是最大距离
                max_distance = math.hypot(screen.get_width(), screen.get_height())
                move_speed = calculate_sun_move_speed(distance, max_distance)
                if distance < move_speed:
                    # 太阳到达目标位置
                    sun['rect'].center = (sun['target_x'], sun['target_y'])
                    sun['moving'] = False
                    self.suns.remove(sun)
                    self.sun_count += self.SUN_VALUE
                else:
                    # 继续移动太阳
                    sun['rect'].centerx += move_speed * dx / distance
                    sun['rect'].centery += move_speed * dy / distance
                    self.draw_sun(screen, sun['rect'].center)
            else:
                # 太阳正在下落
                sun['rect'].y += SUN_FALL_SPEED
                if sun['rect'].bottom > self.screen_height:
                    self.suns.remove(sun)
                else:
                    self.draw_sun(screen, sun['rect'].center)

    def draw_sun(self, screen, position):#绘制太阳
        pygame.draw.circle(screen, YELLOW, position, 1.1*SUN_RADIUS)
        for i in range(NUM_RAYS):
            angle = (i * (2 * math.pi / NUM_RAYS)) + self.rotation_angle
            end_x = position[0] + (SUN_RADIUS * 2) * math.cos(angle)
            end_y = position[1] + (SUN_RADIUS * 2) * math.sin(angle)
            pygame.draw.line(screen, YELLOW, position, (end_x, end_y))
        # 更新太阳的旋转角度
        self.rotation_angle += SUN_ROTATION_SPEED

    def collect_sun(self, mouse_pos):#收集太阳
        for sun in self.suns[:]:
            if sun['rect'].collidepoint(mouse_pos):
                # 太阳开始移动到太阳卡槽
                sun['target_x'] = self.sun_slot_position[0]
                sun['target_y'] = self.sun_slot_position[1]
                sun['moving'] = True

    def draw_sun_count(self, screen):#绘制太阳数量
        sun_text = self.font.render(f'Sun: {self.sun_count}', True, YELLOW)
        sun_text_rect = sun_text.get_rect(center=(50, 70 + sun_text.get_height() // 2))
        screen.blit(sun_text, sun_text_rect)

    def handle_events(self, event):#识别鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.collect_sun((mouse_x, mouse_y))

    def update(self, screen):#每帧更新总处理
        self.generate_suns()
        self.update_suns(screen)
        self.draw_sun_count(screen)