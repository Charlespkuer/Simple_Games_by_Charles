import pygame
import sys
import subprocess
import color
import math
import random
import player_attribute
import background

bullet_damage = player_attribute.bullet['damage']
player_health = player_attribute.player['health']
bullet_rate = player_attribute.bullet['rate']
player_speed = player_attribute.player['speed']
zombie_speed = player_attribute.zombie['speed']
zombie_health = player_attribute.zombie['health']
zombie_freq = player_attribute.zombie['frequency']
rare_options_used = []  # 用于跟踪已使用的稀有选项

class Player:
    def __init__(self, player_position):
        self.width = player_attribute.player['width']
        self.height = player_attribute.player['height']
        self.dodge = player_attribute.player['dodge']
        self.rect = pygame.Rect(player_position[0] - self.width//2, player_position[1] - self.height//2, self.width, self.height)
    
    def draw(self, screen): # 绘制玩家
        pygame.draw.rect(screen, player_attribute.player['color'], self.rect, player_attribute.player['thick']) # 外框架
        #眼睛
        eye_radius = player_attribute.player['eyeradius']
        eye_offset_x = self.rect.width // 5
        eye_center_x = self.rect.centerx
        eye_center_y = self.rect.centery - self.rect.width // 8
        pygame.draw.circle(screen, player_attribute.player['eyecolor'], (eye_center_x - eye_offset_x, eye_center_y), eye_radius)
        pygame.draw.circle(screen, player_attribute.player['eyecolor'], (eye_center_x + eye_offset_x, eye_center_y), eye_radius)

    def mouse_update(self, target): # 移动玩家
        if target is None:
            return None
        else:
            x_move = target[0] - self.rect.centerx
            y_move = target[1] - self.rect.centery
            dist_m = math.hypot(x_move, y_move)
            if dist_m > 0:
                step = min(dist_m, player_speed)
                self.rect.centerx += x_move / dist_m * step
                self.rect.centery += y_move / dist_m * step
                return target
            else:
                return None

    def keyboard_update(self, screen, keys): # 键盘控制
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= player_speed
        if keys[pygame.K_s]: dy += player_speed
        if keys[pygame.K_a]: dx -= player_speed
        if keys[pygame.K_d]: dx += player_speed
        if dx != 0 and dy != 0: dx, dy = dx * 0.7, dy * 0.7
        self.rect.centerx = max(min(self.rect.centerx + dx, screen.get_width() - 0.5*self.width), 0.5*self.width)
        self.rect.centery = max(min(self.rect.centery + dy, screen.get_height() - 0.5*self.height), 0.5*self.height)

    def shoot(self, target, keys, tracking): # 增加待射击子弹参数
        if target is None:
            return Bullet(self.rect, 0, keys, tracking)
        else:
            x_shoot = target[0] - self.rect.centerx
            y_shoot = target[1] - self.rect.centery
            angle = math.atan2(y_shoot, x_shoot)
            if math.hypot(x_shoot, y_shoot) > 0:
                return Bullet(self.rect, angle, keys, tracking)
        
class Bullet:
    def __init__(self, rect, angle, keys, tracking):
        self.keys = keys
        self.width = player_attribute.bullet['width']
        self.height = player_attribute.bullet['height']
        self.radius = 4 + bullet_damage*0.2
        self.bullet_speed = player_attribute.bullet['speed']
        self.range = player_attribute.bullet['range']
        self.angle = angle
        self.rect = pygame.Rect(rect.centerx, rect.centery, self.width, self.height)
        self.tracking = tracking

    def mouse_update(self):
        self.rect.centerx += self.bullet_speed * math.cos(self.angle)
        self.rect.centery += self.bullet_speed * math.sin(self.angle)
    
    def judge_keyboard(keys):
        if keys is None or sum([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]) not in [1, 2]:
            return False
        # 对于两个按键同时按下的情况，只有当它们是对角方向时才返回True
        return not (keys[pygame.K_UP] and keys[pygame.K_DOWN]) and not (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT])
    
    def keyboard_update(self, target):
        if self.tracking == False:
            # 初始化x和y方向上的速度变化为0
            dx = dy = 0
            # 根据按键状态更新x和y方向上的速度变化
            if self.keys[pygame.K_UP]:
                dy -= self.bullet_speed
            if self.keys[pygame.K_DOWN]:
                dy += self.bullet_speed
            if self.keys[pygame.K_LEFT]:
                dx -= self.bullet_speed
            if self.keys[pygame.K_RIGHT]:
                dx += self.bullet_speed
            if dx != 0 and dy != 0:
                dx *= 0.7
                dy *= 0.7
            self.rect.centerx += dx
            self.rect.centery += dy
        else:
            # 计算子弹与目标的角度
            x_move = target[0] - self.rect.centerx
            y_move = target[1] - self.rect.centery
            angle = math.atan2(y_move, x_move)
            # 根据角度更新子弹的位置
            self.rect.centerx += self.bullet_speed * math.cos(angle)
            self.rect.centery += self.bullet_speed * math.sin(angle)

    def judge(self, screen):
        if self.rect.centerx < 0 or self.rect.centerx > screen.get_width() or self.rect.centery < 0 or self.rect.centery > screen.get_height():
            return False
        else:
            return True

    def draw(self, screen):
        pygame.draw.circle(screen, color.black, self.rect.center, self.radius)

class Zombie:
    def __init__(self, screen, player):
        self.width = player_attribute.zombie['width']
        self.height = player_attribute.zombie['height']
        self.speed = zombie_speed
        self.color = player_attribute.zombie['bodycolor']
        self.health = zombie_health
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def random_spawn(self, screen):
        # 从屏幕外边缘的所有位置随机生成僵尸
        edge = random.choice(['top', 'right', 'bottom', 'left'])
        if edge == 'top':
            self.rect.centerx = random.randint(0, screen.get_width())
            self.rect.centery = -self.height // 2
        elif edge == 'right':
            self.rect.centerx = screen.get_width() + self.width // 2
            self.rect.centery = random.randint(0, screen.get_height())
        elif edge == 'bottom':
            self.rect.centerx = random.randint(0, screen.get_width())
            self.rect.centery = screen.get_height() + self.height // 2
        elif edge == 'left':
            self.rect.centerx = -self.width // 2
            self.rect.centery = random.randint(0, screen.get_height())

    def update(self, player):
        direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery).normalize()
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def init_game():
    try:
        # 使用当前Python解释器启动新的程序实例
        subprocess.Popen([sys.executable] + sys.argv)
        # 退出当前程序
        sys.exit(0)
    except Exception as e:
        print(f"Failed to restart the program: {e}")

def game_over(screen):
    running = True
    while running:
        screen.fill(color.gray)
        font = pygame.font.SysFont(None, 120)
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
        screen.blit(text, text_rect)

        button_font = pygame.font.SysFont(None, 50)
        # restart按钮
        restart_text = button_font.render('restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 20))
        restart_bg = pygame.Surface((restart_rect.width + 20, restart_rect.height + 20))
        restart_bg.fill((50, 50, 200))
        restart_bg_rect = restart_bg.get_rect(center=restart_rect.center)
        screen.blit(restart_bg, restart_bg_rect)
        screen.blit(restart_text, restart_rect)

        # quit按钮
        quit_text = button_font.render('quit', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))
        quit_bg = pygame.Surface((quit_rect.width + 20, quit_rect.height + 20))
        quit_bg.fill((200, 50, 50))
        quit_bg_rect = quit_bg.get_rect(center=quit_rect.center)
        screen.blit(quit_bg, quit_bg_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_bg_rect.collidepoint(event.pos):
                    return 'restart'
                elif quit_bg_rect.collidepoint(event.pos):
                    pygame.quit()
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

def apply_boost(screen, options):
    paused = True
    selected_option = None
    button_font = pygame.font.SysFont(None, 24)
    button_width, button_height = 150, 50
    button_spacing = 20
    total_width = (button_width + button_spacing) * len(options) - button_spacing
    start_x = (screen.get_width() - total_width) // 2
    start_y = (screen.get_height() - button_height) // 2

    buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect(start_x + (button_width + button_spacing) * i, start_y, button_width, button_height)
        buttons.append((button_rect, option))

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (button_rect, option) in enumerate(buttons):
                    if button_rect.collidepoint(event.pos):
                        selected_option = option
                        paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    selected_option = options[event.key - pygame.K_1]
                    paused = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (100, 100, 100), (start_x - 10, start_y - 10, total_width + 20, button_height + 20))
        for i, (button_rect, option) in enumerate(buttons):
            pygame.draw.rect(screen, (200, 200, 200), button_rect)
            text = button_font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            if selected_option == option:
                pygame.draw.rect(screen, (0, 255, 0), button_rect, 3)
        pygame.display.flip()
    # Apply the selected boost
    if selected_option == "health+20":
        global player_health
        player_health += 20
    elif selected_option == "attack+5":
        global bullet_damage 
        bullet_damage += 5
    elif selected_option == "attack rate+0.5":
        global bullet_rate
        bullet_rate +=0.5
    elif selected_option == "speed+0.5":
        global player_speed
        player_speed += 0.5
    elif selected_option == "zombie speed-0.1":
        global zombie_speed
        zombie_speed -= 0.1
    elif selected_option == "zombie health*90%":
        global zombie_health
        zombie_health *=0.9
    elif selected_option == "tracking bullet":
        rare_options_used.append("tracking bullet")
    elif selected_option == "zombie frequency-0.5":
        global zombie_freq
        zombie_freq -= 0.5

def main():
    pygame.init() # 初始化
    screen = pygame.display.set_mode((900, 600)) # 
    pygame.display.set_caption("player1") # 设置标题
    clock = pygame.time.Clock() # 设置时钟

    player1 = Player([0.5*screen.get_width(), 0.5*screen.get_height()]) # 创建玩家
    target = None
    zombie_kills = 0
    zombies, bullets = [], [] # 僵尸与子弹列表
    bullet_last_spawn, zombie_spawn_time = 0, 0
    running = True

    while running:
        background.generate_weeds(screen, 100)

        if pygame.event.get(pygame.QUIT): running = False
        
        global zombie_speed, zombie_health, zombie_freq
        keys = pygame.key.get_pressed()
        player1.keyboard_update(screen, keys)
        current_time = pygame.time.get_ticks()
        if Bullet.judge_keyboard(keys) and current_time - bullet_last_spawn > 1000 / bullet_rate:
            if "tracking bullet"  in rare_options_used:
                bullet = player1.shoot(target, keys, True)
            else:
                bullet = player1.shoot(None, keys, False)
            bullet_last_spawn = pygame.time.get_ticks()
            if bullet: bullets.append(bullet)

        if current_time - zombie_spawn_time > 10000// zombie_freq:
            zombie = Zombie(screen, player1)
            zombies.append(zombie)
            zombie.random_spawn(screen)
            zombie_spawn_time = current_time

        # 在游戏主循环中处理子弹与僵尸的碰撞
        for bullet in bullets[:]: 
            for zombie in zombies[:]: 
                if bullet.rect.colliderect(zombie.rect):  # 检测子弹与僵尸的碰撞
                    zombie.health -= bullet_damage
                    bullets.remove(bullet) 
                    if zombie.health <= 0:
                        zombies.remove(zombie)
                        zombie_kills += 1
                    break
        # 在游戏主循环中处理僵尸与玩家的碰撞
        for zombie in zombies[:]: 
            if zombie.rect.colliderect(player1.rect):  # 检测僵尸与玩家的碰撞
                global player_health
                player_health -= 10 
                zombies.remove(zombie)  # 从僵尸列表中移除碰撞的僵尸
                if player_health <= 0:  # 如果玩家血量归零
                    # 触发游戏结束逻辑，比如切换到“Game Over”界面sd
                    result = game_over(screen) 
                    if result == 'restart':
                        init_game()
                    break
        
        if zombie_kills % 5 == 0 and zombie_kills != 0:
            options = ["health+20", "attack+5", "attack rate+0.5", "speed+0.5", "zombie speed-0.1", "zombie health*90%","zombie frequency-0.5"]
            if "tracking bullet" not in rare_options_used and random.randint(1, 10) == 1:
                options.append("tracking bullet")
            selected_options = random.sample(options, 3)
            apply_boost(screen, selected_options)
            if "tracking bullet" in selected_options and "1" not in rare_options_used:
                rare_options_used.append("1")
            zombie_health += player_attribute.zombie['health_up']
            zombie_freq += 0.1
            zombie_kills += 1

        #绘图部分
        player1.draw(screen)

        for zombie in zombies:
            zombie.update(player1)
            zombie.draw(screen)

        if target:
            target = player1.mouse_update(screen, target)   
        for bullet in bullets:
            if "tracking bullet"  in rare_options_used:
                #计算所有僵尸距离玩家最近的一个
                closest_zombie = min(zombies, key=lambda z: pygame.math.Vector2(z.rect.center).distance_to(player1.rect.center))
                bullet.keyboard_update(closest_zombie.rect.center)
            else:
                bullet.keyboard_update(None)
            bullet.draw(screen)
            if not bullet.judge(screen):
                bullets.remove(bullet)
        
        font = pygame.font.SysFont(None, 24)  # 创建字体对象
        kill_count_text = font.render(f'Kills: {int(zombie_kills)}', True, (255, 255, 255))  
        screen.blit(kill_count_text, (10, screen.get_height() - 30))  
        health_text = font.render(f'Health: {int(player_health)}', True, (255, 255, 255))
        screen.blit(health_text, (10, screen.get_height() - 60))
        attack_text = font.render(f'Attack: {int(bullet_damage)}', True, (255, 255, 255))
        screen.blit(attack_text, (10, screen.get_height() - 90))
        attack_rate_text = font.render(f'Attack Rate: {bullet_rate:.1f}', True, (255, 255, 255))
        screen.blit(attack_rate_text, (10, screen.get_height() - 120))
        speed_text = font.render(f'Speed: {player_speed}', True, (255, 255, 255))
        screen.blit(speed_text, (10, screen.get_height() - 150))
        zombie_speed_text = font.render(f'Zombie Speed: {zombie_speed:.1f}', True, (255, 255, 255))
        screen.blit(zombie_speed_text, (10, screen.get_height() - 180))
        zombie_health_text = font.render(f'Zombie Health: {int(zombie_health)}', True, (255, 255, 255))
        screen.blit(zombie_health_text, (10, screen.get_height() - 210))
        zombie_freq_text = font.render(f'Zombie Frequency: {zombie_freq:.1f}', True, (255, 255, 255))
        screen.blit(zombie_freq_text, (10, screen.get_height() - 240))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()