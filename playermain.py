import pygame
import color
import player
import player_attribute


screen = pygame.display.set_mode((900, 600)) # 
player1 = player.Player([0.5*screen.get_width(), 0.5*screen.get_height()]) # 创建玩家
target = None
bullets = [] # 储存子弹信息
fire_rate = player_attribute.bullet['rate']

pygame.init() # 初始化
pygame.display.set_caption("player1") # 设置标题
clock = pygame.time.Clock() # 设置时钟
bullet_last_spawn = pygame.time.get_ticks()
running = True

while running:
    screen.fill(color.white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = player1.shoot(event.pos, None) # 向函数中添加
                if bullet:
                    bullets.append(bullet) # 向列表中添加
            elif event.button == 3:
                target = event.pos
    keys = pygame.key.get_pressed()
    player1.keyboard_update(screen, keys)
    if (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])and pygame.time.get_ticks() - bullet_last_spawn > 1000/fire_rate:
        bullet = player1.shoot(None, keys)
        bullet_last_spawn = pygame.time.get_ticks()
        if bullet:
            bullets.append(bullet)
    player1.draw(screen)
    if target:
        target = player1.mouse_update(screen, target)   
    for bullet in bullets:
        #bullet.mouse_update(screen)
        bullet.keyboard_update(screen)
        if not bullet.judge(screen):
            bullets.remove(bullet)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()