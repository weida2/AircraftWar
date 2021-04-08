import pygame
import sys
import traceback
import myplane
import enemy
import bullet
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# 设置游戏屏幕窗口大小以及背景图片
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战--打飞机')

background = pygame.image.load('images/background.png').convert()

# 载入游戏音乐
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
button_sound = pygame.mixer.Sound('sound/button.wav')
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_flying_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
supply_sound = pygame.mixer.Sound('sound/supply.wav')
upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
use_bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')

bullet_sound.set_volume(0.2)
button_sound.set_volume(0.2)
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound.set_volume(0.2)
get_bomb_sound.set_volume(0.2)
get_bullet_sound.set_volume(0.2)
me_down_sound.set_volume(0.2)
supply_sound.set_volume(0.2)
upgrade_sound.set_volume(0.2)
use_bomb_sound.set_volume(0.2)

# 定义颜色

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

# 主函数部分


def main():
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    running = True

    # 生成我方飞机
    me = myplane.MyPlane(bg_size)

    # 生成敌方飞机  小中大
    enenmies = pygame.sprite.Group()

    small_enenmies = pygame.sprite.Group()
    add_small_enemies(small_enenmies, enenmies, 15)

    mid_enenmies = pygame.sprite.Group()
    add_mid_enemies(mid_enenmies, enenmies, 4)

    big_enenmies = pygame.sprite.Group()
    add_big_enemies(big_enenmies, enenmies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 10
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 用于切换图片
    switch_image = True

    # 增加延迟
    delay = 100

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top =  width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

        # 绘制背景图片
        screen.blit(background, (0, 0))

        if not paused:

            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 发射子弹
            if not (delay % 10):
                bullet1[bullet1_index].reset(me.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机:
            for b in bullet1:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enenmies, False, pygame.sprite.collide_mask) # 被子弹击中的敌机
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enenmies or e in big_enenmies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            # 绘制敌方战机

                # 大型飞机
            for each in big_enenmies:
                if each.active:
                    each.move()
                    if each.hit:
                        # 绘制被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.left, each.rect.top - 5),\
                                     2)

                    # 当生命大于 20 % 显示绿色， 否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,\
                                     (each.rect.left, each.rect.top - 5),\
                                     (each.rect.left + each.rect.width * energy_remain,\
                                      each.rect.top - 5), 2)

                    # 即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        enemy3_flying_sound.play(-1)

                else:
                    # 飞机毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_flying_sound.stop()
                            score += 10000
                            each.reset()

                # 中型飞机
            for each in mid_enenmies:
                if each.active:
                    each.move()
                    if each.hit:
                        # 绘制被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left, each.rect.top - 5), \
                                     2)

                    # 当生命大于 20 % 显示绿色， 否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)

                else:
                    # 飞机毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

                # 小型飞机
            for each in small_enenmies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

                else:
                    # 飞机毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)

            else:
                # 飞机毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if not me_destroy_index:
                        print('Game Over!')
                        running = not running

        # 绘制得分板

        score_text = score_font.render('Score : %s' % str(score), True, WHITE)
        screen.blit(score_text, (10, 5))

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 检测我方飞机是否被撞

        enenmies_down = pygame.sprite.spritecollide(me, enenmies, False, pygame.sprite.collide_mask)  # 被撞中的敌机

        if enenmies_down:
        #   me.active = False
            for e in enenmies_down:
                e.active = False
        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input('游戏异常退出，请点击任意按键退出程序')

