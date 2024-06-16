# zombie.py
import pygame
import random

BLACK = (0, 0, 0)

class Zombie:
    def __init__(self, screen):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = pygame.font.SysFont(None, 36)  # 字体
        self.zombies = []
        self.width = 50
        self.height = 50
        self.kill_count = 0 # 初始击杀数目
        self.zombie_speed0 = 0.6  # 设置僵尸的移动速度
        self.zombie_speed_random_range = 0.3  # 僵尸速度随机范围
        self.zombie_spawn_interval = 500  # 单位毫秒，初始生成频率
        self.min_spawn_interval = 300  # 最小生成频率
        self.spawn_interval_decrease_rate = 0.01  # 生成频率递减速率
        self.spawn_interval_random_range = 200  # 生成频率随机范围
        self.last_zombie_spawn_time = pygame.time.get_ticks()

    def generate_zombies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_zombie_spawn_time > self.zombie_spawn_interval:
            self.last_zombie_spawn_time = current_time
            zombie_x = self.screen_width  # 从屏幕右侧边缘生成
            zombie_y = random.randint(-3, 3) * 1.5 * self.height + self.screen_height * 0.5  # 随机生成y坐标
            zombie_type = random.choice(['zombie1', 'zombie2','zombie3'])  # 随机选择僵尸类型
            if zombie_type == 'zombie1':
                zombie_speed = self.zombie_speed0 - 0.3
            elif zombie_type == 'zombie2':
                zombie_speed = self.zombie_speed0
            elif zombie_type == 'zombie3':
                zombie_speed = self.zombie_speed0 + 0.5
           # zombie_speed += self.zombie_speed_random_range * (random.random() * 2 - 1)  # 设置随机速度
            self.zombies.append({'rect': pygame.Rect(zombie_x, zombie_y, self.width, self.height), 'speed': zombie_speed, 'type': zombie_type})  # 僵尸大小、速度、种类
            # 更新生成频率
            self.zombie_spawn_interval -= self.spawn_interval_decrease_rate * self.zombie_spawn_interval
            self.temp_zombie_spawn_interval = self.zombie_spawn_interval + random.randint(-self.spawn_interval_random_range, self.spawn_interval_random_range)
            self.zombie_spawn_interval = max(self.min_spawn_interval, self.temp_zombie_spawn_interval)

    def draw_zombie1(self, screen, zombie):
        # 绘制僵尸的头部
        pygame.draw.rect(screen, (92, 64, 51), zombie)  # 深棕色头部
        # 绘制眼睛
        eye_width = zombie.width // 10
        eye_height = zombie.height // 10
        eye_offset_x = zombie.width // 10
        eye_offset_y = zombie.height // 4
        left_eye_rect = pygame.Rect(zombie.x + eye_offset_x, zombie.y + eye_offset_y, eye_width, eye_height)
        right_eye_rect = pygame.Rect(zombie.x + zombie.width - eye_offset_x - eye_width, zombie.y + eye_offset_y, eye_width, eye_height)
        pygame.draw.rect(screen, (255, 0, 0), left_eye_rect)  # 红色的方形眼睛
        pygame.draw.rect(screen, (255, 0, 0), right_eye_rect)  # 红色的方形眼睛
        # 绘制嘴巴
        mouth_width = zombie.width // 2
        mouth_height = zombie.height // 5
        mouth_offset_x = zombie.width // 4
        mouth_offset_y = zombie.height // 2
        mouth_rect = pygame.Rect(zombie.x + mouth_offset_x, zombie.y + zombie.height - mouth_offset_y, mouth_width, mouth_height)
        pygame.draw.rect(screen, (0, 0, 0), mouth_rect)  # 黑色的口腔
        # 绘制牙齿
        tooth_width = mouth_width // 4
        tooth_height = mouth_height // 2
        tooth_offset_x = tooth_width // 2
        tooth_offset_y = tooth_height // 2
        tooth_rect_left_top = pygame.Rect(mouth_rect.x + tooth_offset_x, mouth_rect.y + tooth_offset_y-2, tooth_width, tooth_height)
        tooth_rect_right_bottom = pygame.Rect(mouth_rect.x + mouth_width - tooth_offset_x - tooth_width, mouth_rect.y + mouth_height - tooth_height - tooth_offset_y+2, tooth_width, tooth_height)
        pygame.draw.rect(screen, (255, 255, 255), tooth_rect_left_top)  # 白色的左上角牙齿
        pygame.draw.rect(screen, (255, 255, 255), tooth_rect_right_bottom)  # 白色的右下角牙齿

    def draw_zombie2(self, screen, zombie):
        # 绘制僵尸的头部
        pygame.draw.rect(screen, (0, 128, 0), zombie)  # 深绿色头部
        # 绘制眼睛
        eye_width = zombie.width // 10
        eye_height = zombie.height // 10
        eye_offset_x = zombie.width // 10
        eye_offset_y = zombie.height // 4
        left_eye_rect = pygame.Rect(zombie.x + eye_offset_x, zombie.y + eye_offset_y, eye_width, eye_height)
        right_eye_rect = pygame.Rect(zombie.x + zombie.width - eye_offset_x - eye_width, zombie.y + eye_offset_y, eye_width, eye_height)
        pygame.draw.rect(screen, (255, 255, 255), left_eye_rect)  # 白色的方形眼睛
        pygame.draw.rect(screen, (255, 255, 255), right_eye_rect)  # 白色的方形眼睛
        # 绘制嘴巴
        mouth_width = zombie.width // 2
        mouth_height = zombie.height // 5
        mouth_offset_x = zombie.width // 4
        mouth_offset_y = zombie.height // 2
        mouth_rect = pygame.Rect(zombie.x + mouth_offset_x, zombie.y + zombie.height - mouth_offset_y, mouth_width, mouth_height)
        pygame.draw.rect(screen, (0, 0, 0), mouth_rect)  # 黑色的口腔
        # 绘制牙齿
        tooth_width = mouth_width // 4
        tooth_height = mouth_height // 2
        tooth_offset_x = tooth_width // 2
        tooth_offset_y = tooth_height // 2
        tooth_rect_left_top = pygame.Rect(mouth_rect.x + tooth_offset_x, mouth_rect.y + tooth_offset_y-2,tooth_width, tooth_height)
        tooth_rect_right_bottom = pygame.Rect(mouth_rect.x + mouth_width - tooth_offset_x - tooth_width, mouth_rect.y + mouth_height - tooth_height - tooth_offset_y+2, tooth_width, tooth_height)
        pygame.draw.rect(screen, (255, 255, 255), tooth_rect_left_top)  # 白色的左上角牙齿
        pygame.draw.rect(screen, (255, 255, 255), tooth_rect_right_bottom)  # 白色的右下角牙齿

    def draw_zombie3(self, screen, zombie):
        # 绘制僵尸的头部
        pygame.draw.ellipse(screen, (0, 128, 0), zombie)  # 椭圆形头部
        # 绘制眼睛
        eye_width = zombie.width // 7
        eye_height = zombie.height // 5
        eye_offset_x = zombie.width // 5
        eye_offset_y = zombie.height // 2.5
        left_eye_rect = pygame.Rect(zombie.x + eye_offset_x, zombie.y + eye_offset_y, eye_width, eye_height)
        right_eye_rect = pygame.Rect(zombie.x + zombie.width - eye_offset_x - eye_width, zombie.y + eye_offset_y, eye_width, eye_height)
        pygame.draw.ellipse(screen, (255, 0, 0), left_eye_rect)  # 红色的椭圆形眼睛
        pygame.draw.ellipse(screen, (255, 0, 0), right_eye_rect)  # 红色的椭圆形眼睛
        # 绘制嘴巴
        mouth_width = zombie.width // 3
        mouth_height = zombie.height // 5
        mouth_offset_x = zombie.width // 3
        mouth_offset_y = zombie.height // 2
        mouth_top = (zombie.x + zombie.width/2, zombie.y + zombie.height - mouth_height)
        mouth_left = (zombie.x + mouth_offset_x, zombie.y + zombie.height - mouth_offset_y + mouth_height)
        mouth_right = (zombie.x + mouth_offset_x + mouth_width, zombie.y + zombie.height - mouth_offset_y + mouth_height)
        pygame.draw.polygon(screen, (0, 0, 0), [mouth_top, mouth_left, mouth_right])  # 黑色的倒三角形嘴巴

    def kill_zombie(self, mouse_pos):#击杀僵尸
        for zombie in self.zombies[:]:
            if zombie['rect'].collidepoint(mouse_pos):
                self.zombies.remove(zombie)
                self.kill_count += 1

    def draw_kill_count(self, screen):#绘制击杀数目
        kill_text = self.font.render(f'Kill: {self.kill_count}', True, BLACK)
        kill_text_rect = kill_text.get_rect(center=(50, self.screen_height-50 + kill_text.get_height() // 2))
        screen.blit(kill_text, kill_text_rect)

    def handle_events(self, event):#识别鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.kill_zombie((mouse_x, mouse_y))

    def update_zombies(self, screen):
        for zombie in self.zombies[:]:
            zombie['rect'].x -= zombie['speed'] #+ 2*random.random()   # 使用僵尸的速度来移动
            if zombie['rect'].right < 0:  # 如果僵尸完全离开屏幕，则移除
                self.zombies.remove(zombie)
            else:
                if zombie['type'] == 'zombie1':
                    self.draw_zombie1(screen,zombie['rect'] )
                elif zombie['type'] == 'zombie2':
                    self.draw_zombie2(screen, zombie['rect'])
                elif zombie['type'] == 'zombie3':
                    self.draw_zombie3(screen, zombie['rect'])