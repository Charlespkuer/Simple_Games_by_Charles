import pygame
import random
import background  # 导入 weed_generator 模块

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 定义屏幕大小
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# 定义僵尸类
class Zombie:
    def __init__(self, type, speed):
        self.type = type
        self.speed = speed
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH
        self.y = random.randint(0 + self.height, SCREEN_HEIGHT - 2*self.height)

    def update(self, screen):
        self.x -= self.speed
        # 绘制图像
        if self.type == 'zombie1':
            pygame.draw.rect(screen, BLACK, (int(self.x), int(self.y), 50, 50))
        elif self.type == 'zombie2':
            pygame.draw.rect(screen, BLUE, (int(self.x), int(self.y), 50, 50))
        elif self.type == 'zombie3':
            pygame.draw.rect(screen, RED, (int(self.x), int(self.y), 50, 50))

# 定义僵尸管理器类
class ZombieManager:
    def __init__(self):
        self.zombies = []
        self.freq = 800  # 单位毫秒，初始生成频率
        self.min_freq = 400  # 最小生成频率
        self.freq_decrease = 0.01  # 生成频率递减速率
        self.freq_random = 200  # 生成频率随机范围
        self.last_spawn = pygame.time.get_ticks()

    def generate_zombies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > self.freq:
            self.last_spawn = current_time
            type = random.choice(['zombie1', 'zombie2', 'zombie3'])
            if type == 'zombie1':
                speed = 0.8
            elif type == 'zombie2':
                speed = 1.0
            elif type == 'zombie3':
                speed = 1.2
            self.zombies.append(Zombie(type, speed))
            # 更新生成频率
            self.freq -= self.freq_decrease * self.freq
            self.freq = max(self.min_freq, self.freq + random.randint(-self.freq_random, self.freq_random))

    def update_zombies(self, screen):
        for zombie in self.zombies:
            if zombie.x < -50:
                self.zombies.remove(zombie)
            else:
                zombie.update(screen)

# 主函数
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Apocalypse")

    clock = pygame.time.Clock()
    running = True

    zombie_manager = ZombieManager()

    # 创建一个新的 Surface 对象来存储杂草
    weeds = pygame.Surface(screen.get_size())

    # 在游戏开始时生成杂草
    background.generate_weeds(weeds, 100)  # 生成100个小杂草 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(weeds, (0, 0))  # 将杂草绘制到屏幕上

        # 生成并更新僵尸
        zombie_manager.generate_zombies()
        zombie_manager.update_zombies(screen)

        pygame.display.flip()  # 更新整个屏幕
        clock.tick(60)  # 控制游戏帧率

    pygame.quit()

if __name__ == "__main__":
    main()