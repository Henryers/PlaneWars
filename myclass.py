# 对项目所需的类进行定义（根据需要在其他的模块中继承）

import pygame
import random
import time
# 引入按键事件等，后续代码可以省略模块前缀
from pygame.locals import *


# 1. 玩家飞机类
class Player(pygame.sprite.Sprite):
    # 存放所有飞机子弹的组
    bullets = pygame.sprite.Group()

    def __init__(self, screen, mode):
        # 这个精灵类的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # 模式mode1：无尽endless模式的飞机，获得暂时强化补给
        # 模式mode2：副本boss模式的飞机，获得累加的强化补给
        self.mode = mode
        # 飞机
        self.plane = pygame.image.load("./image/player.png")
        # 根据图片，获取矩形对象
        self.rect = self.plane.get_rect()  # rect矩形
        # 设置飞机/矩形位置
        self.rect.center = [240, 550]

        self.speed = 10

        self.screen = screen

        # 装子弹的列表
        self.bullets = pygame.sprite.Group()

        # 记录上次发射子弹的时间点
        self.last_bullet_time = pygame.time.get_ticks()
        self.shoot_interval = 200  # 200毫秒为子弹的发射间隔

        # 补给时间点
        self.supply_collected_time = 0

    # 检验按键处理相关事件
    def key_control(self):
        key_pressed = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # 按下当前键的时间点

        if (key_pressed[K_w] or key_pressed[K_UP]) and self.rect.top > -20:
            self.rect.top -= self.speed
        if (key_pressed[K_s] or key_pressed[K_DOWN]) and self.rect.bottom < 720:
            self.rect.bottom += self.speed
        if (key_pressed[K_a] or key_pressed[K_LEFT]) and self.rect.left > -20:
            self.rect.left -= self.speed
        if (key_pressed[K_d] or key_pressed[K_RIGHT]) and self.rect.right < 500:
            self.rect.right += self.speed
        if key_pressed[K_SPACE] and current_time - self.last_bullet_time > self.shoot_interval:
            # 每次发射子弹都要重置计时器，这样才能控制发射间隔
            self.last_bullet_time = current_time
            # 无尽模式的两种子弹状态
            if self.mode == 0:
                # 无尽模式的补给：判断是否过了10秒
                if time.time() - self.supply_collected_time < 10:
                    self.shoot2()  # 发射两个弹道
                else:
                    self.shoot1()  # 发射一个弹道
            # boss模式的四种子弹状态
            elif self.mode == 1:
                self.shoot1()
            elif self.mode == 2:
                self.shoot2()
            elif self.mode == 3:
                self.shoot3()
            elif self.mode == 4:
                self.shoot4()

    # 按下空格键且满足时间间隔时，调用发射子弹的函数
    def shoot1(self):
        # （子弹坐标和飞机有关联，需要传入2个飞机的矩形位置参数）
        bullet = Bullet1(self.screen, self.rect.centerx, self.rect.top)
        # 把子弹放进列表里
        self.bullets.add(bullet)
        # 加到存放所有飞机子弹的组
        Player.bullets.add(bullet)

    def shoot2(self):
        # top-8是为了让纵坐标区分开，否则两颗子弹同时击中只能被系统判定为一次碰撞而已
        bullet1 = Bullet1(self.screen, self.rect.centerx - 15, self.rect.top-8)
        bullet2 = Bullet1(self.screen, self.rect.centerx + 15, self.rect.top)
        self.bullets.add(bullet1)
        self.bullets.add(bullet2)
        Player.bullets.add(bullet1)
        Player.bullets.add(bullet2)

    def shoot3(self):
        # （子弹坐标和飞机有关联，需要传入2个飞机的矩形位置参数）
        bullet = Bullet2(self.screen, self.rect.centerx, self.rect.top)
        bullet1 = Bullet3LSlow(self.screen, self.rect.centerx - 15, self.rect.top - 8)
        bullet2 = Bullet3RSlow(self.screen, self.rect.centerx + 15, self.rect.top)
        # 把子弹放进列表里
        self.bullets.add(bullet)
        self.bullets.add(bullet1)
        self.bullets.add(bullet2)
        # 存放所有飞机子弹的组
        Player.bullets.add(bullet)
        Player.bullets.add(bullet1)
        Player.bullets.add(bullet2)

    def shoot4(self):
        # （子弹坐标和飞机有关联，需要传入2个飞机的矩形位置参数）
        bullet1 = Bullet2(self.screen, self.rect.centerx-12, self.rect.top)
        bullet2 = Bullet2(self.screen, self.rect.centerx+12, self.rect.top)
        bullet_l = Bullet3LFast(self.screen, self.rect.centerx - 20, self.rect.top-20)
        bullet_r = Bullet3RFast(self.screen, self.rect.centerx + 20, self.rect.top)
        # 把子弹放进列表里
        self.bullets.add(bullet1)
        self.bullets.add(bullet2)
        self.bullets.add(bullet_l)
        self.bullets.add(bullet_r)
        # 存放所有飞机子弹的组
        Player.bullets.add(bullet1)
        Player.bullets.add(bullet2)
        Player.bullets.add(bullet_l)
        Player.bullets.add(bullet_r)

    def display(self):
        self.screen.blit(self.plane, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()

    @classmethod
    def clear_bullets(cls):
        # 清空子弹
        cls.bullets.empty()


# 2. 玩家子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, path):
        # 这个精灵类的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # 玩家飞机子弹
        self.image = pygame.image.load(f"./image/{path}")
        # 根据图片，获取矩形对象
        self.rect = self.image.get_rect()  # rect矩形
        self.rect.midbottom = [x, y]

        self.speed = 10
        # 窗口
        self.screen = screen

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.top < -20:
            self.kill()


# 3. 玩家子弹子类
class Bullet1(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet1.png')


class Bullet2(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet2.png')


class Bullet3LSlow(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet3.png')

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        self.rect.left -= 1
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()


class Bullet3RSlow(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet3.png')

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        self.rect.left += 1
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()


class Bullet3LFast(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet3.png')
        self.speed = 15

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        self.rect.left -= 1
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()


class Bullet3RFast(Bullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='my_bullet3.png')
        self.speed = 15

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        self.rect.left += 1
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    # 敌方所有子弹
    enemy_bullets = pygame.sprite.Group()

    def __init__(self, screen, hp, speed, path, bg_size):
        # 这个精灵类的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # hp
        self.hp = hp
        # boss
        self.enemy = pygame.image.load(f"./image/{path}")
        # 根据图片，获取矩形对象
        self.rect = self.enemy.get_rect()  # rect矩形

        x = random.randrange(1, bg_size[0], 50)
        self.rect.midbottom = [x, 0]

        self.speed = speed
        # 窗口
        self.screen = screen
        # 装子弹的列表
        self.bullets = pygame.sprite.Group()
        # 敌机移动方向
        self.direction = 'right'

    def display(self):
        self.screen.blit(self.enemy, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def auto_move(self):
        if self.direction == 'right':
            self.rect.right += self.speed
        elif self.direction == 'left':
            self.rect.right -= self.speed

        # 敌机方向改变，防止移出屏幕
        if self.rect.right > 480:
            self.direction = 'left'
        elif self.rect.right < 0:
            self.direction = 'right'
        # 敌机方向随机改变
        random_num = random.randint(1, 100)
        if random_num == 1:
            self.direction = 'left'
        elif random_num == 2:
            self.direction = 'right'

        self.rect.bottom += self.speed

    # 敌机自动开火，随机数决定是否发射，否则每次while都发射，太快啦！
    def auto_fire(self):
        random_num = random.randint(1, 40)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            Enemy.enemy_bullets.add(bullet)

    def update(self, *args, **kwargs):
        self.auto_move()
        self.auto_fire()
        self.display()

    @classmethod
    def clear_bullets(cls):
        # 清空子弹
        cls.enemy_bullets.empty()


# 敌机子弹类
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, path):
        # 这个精灵类的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # 敌机子弹
        self.image = pygame.image.load(f"./image/{path}")
        # 根据图片，获取矩形对象
        self.rect = self.image.get_rect()  # rect矩形
        self.rect.center = [x, y+5]
        self.speed = 3
        # 窗口
        self.screen = screen
    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        # 如果子弹移出屏幕下方，则销毁子弹对象
        if self.rect.top > 700:
            self.kill()


# 地图类
class GameBackground(object):
    # 初始化地图
    def __init__(self, screen, bg_size, path1, path2):
        self.mImage1 = pygame.image.load(f"./image/{path1}")
        self.mImage2 = pygame.image.load(f"./image/{path2}")
        self.mImage3 = pygame.image.load(f"./image/{path1}")
        # 窗口
        self.screen = screen
        # 图片大小
        self.bg_size = bg_size
        # 辅助移动地图
        self.y1 = 0
        self.y2 = -bg_size[1]    # -700
        self.y3 = -bg_size[1]*2  # -1400

    # 绘制地图
    def draw(self):
        self.screen.blit(self.mImage1, (0, self.y1))
        self.screen.blit(self.mImage2, (0, self.y2))
        self.screen.blit(self.mImage3, (0, self.y3))

    # 移动地图
    def move(self):
        self.y1 += 2
        self.y2 += 2
        self.y3 += 2
        # 每次不断自增，代表图片往下移动，第三张移动到第一张的时候，大循环结束，各自初始化为最初位置
        if self.y1 >= self.bg_size[1]*2:
            self.y1 = 0
            self.y2 = -self.bg_size[1]
            self.y3 = -self.bg_size[1]*2


# 补给类
class Supply(pygame.sprite.Sprite):
    def __init__(self, screen, bg_size):
        # 这个精灵类的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # 补给
        self.image = pygame.image.load("./image/supply.png")
        # 根据图片，获取矩形对象
        self.rect = self.image.get_rect()  # rect矩形
        x = random.randrange(1, bg_size[0], 50)
        self.rect.midbottom = [x, 0]
        self.speed = 5
        # 窗口
        self.screen = screen

    def display(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.display()
        # 动态修改补给坐标
        self.rect.top += self.speed
        # 如果补给移出屏幕下方，则销毁补给对象
        if self.rect.top > 700:
            self.kill()


# 爆炸
class Bomb(object):
    # 初始化爆炸
    def __init__(self, screen, typename):
        self.screen = screen
        # 加载爆炸资源
        self.mImages = [
            pygame.image.load(f"./image/{typename}_down" + str(v) + ".png") for v in range(1, 4)
        ]
        # 设置当前爆炸播放索引
        self.mIndex = 0
        # 爆炸位置
        self.mPos = [0, 0]
        # 是否可见
        self.mVisible = False

    # 设置位置
    def action(self, rect):
        # 启动，先初始化爆炸的坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 打开爆炸的开关,触发爆炸方法draw
        self.mVisible = True

    # 绘制爆炸
    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImages[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1  # self.mIndex最初是0，先画出来，位置初始化后不变，之后每画一次爆炸过程，图片索引++，位置不改变
        if self.mIndex >= len(self.mImages):
            # 如果下标已经到最后，代表爆炸结束
            # 下标重置
            self.mIndex = 0
            self.mVisible = False
