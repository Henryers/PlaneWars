# boss模式

import time
import random
import pygame
from pygame.locals import *  # 不引入变量，只引入常量，防止命名冲突
import myclass


# boss两形态继承
class Boss1(myclass.Enemy):
    enemy_bullets = pygame.sprite.Group()  # 创建独立的子弹组

    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=80, speed=2, path="boss1.png", bg_size=(480, 700))
        self.rect.midbottom = [240, 0]

    def auto_move(self):
        if self.rect.bottom < 200:
            self.rect.bottom += self.speed

        # print(self.rect.bottom)  boss下来后再左右移动
        if self.rect.bottom >= 200 and self.direction == 'right':
            self.rect.right += self.speed - 1
        elif self.rect.bottom >= 200 and self.direction == 'left':
            self.rect.right -= self.speed - 1

        # 敌机方向改变，防止移出屏幕
        if self.rect.right > 520:
            self.direction = 'left'
        elif self.rect.left < -40:
            self.direction = 'right'

    # 敌机自动开火，随机数决定是否发射，否则每次while都发射，太快啦！
    def auto_fire(self):
        random_num = random.randint(1, 50)
        random_x = random.randint(self.rect.left + 20, self.rect.right - 20)
        if random_num <= 2 and self.rect.bottom >= 200:
            bullet = BossEnemyBullet1(self.screen, random_x, self.rect.bottom - 20)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            Boss1.enemy_bullets.add(bullet)
        elif random_num <= 5 and self.rect.bottom >= 200:
            bullet = BossEnemyBullet2(self.screen, random_x, self.rect.bottom - 20)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            Boss1.enemy_bullets.add(bullet)


class Boss2(myclass.Enemy):
    enemy_bullets = pygame.sprite.Group()  # 创建独立的子弹组

    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=480, speed=2, path="boss2.png", bg_size=(480, 700))
        self.rect.midbottom = [240, 0]
        self.timer_flag = False
        self.is_fire = False

    def auto_move(self):
        # print(self.rect.bottom)
        if self.rect.bottom >= 200 and self.direction == 'right':
            self.rect.right += self.speed - 1
        elif self.rect.bottom >= 200 and self.direction == 'left':
            self.rect.right -= self.speed - 1

        # 敌机方向改变，防止移出屏幕
        if self.rect.right > 520:
            self.direction = 'left'
        elif self.rect.left < -40:
            self.direction = 'right'

        if self.rect.bottom < 200:
            self.rect.bottom += self.speed

    # 敌机自动开火，随机数决定是否发射，否则每次while都发射，太快啦！
    def auto_fire(self, player_x=0):
        random_num = random.randint(1, 30)
        random_x = random.randint(self.rect.left + 20, self.rect.right - 20)
        if random_num <= 1 and self.rect.bottom >= 200:
            bullet = BossEnemyBullet3(self.screen, random_x, self.rect.bottom - 20)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            Boss2.enemy_bullets.add(bullet)
        elif random_num <= 4 and self.rect.bottom >= 200:
            bullet = BossEnemyBullet4(self.screen, random_x, self.rect.bottom - 20)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            Boss2.enemy_bullets.add(bullet)
        elif random_num <= 5 and self.rect.bottom >= 200 and not self.timer_flag:
            # 先打开定时器，输出一个激光          # 当前无激光绘制才能进行绘制，否则两个激光的不同定时器冲突
            pygame.time.set_timer(Manager.create_bullet_id, 200)
            self.timer_flag = True  # 激光正在绘制
            # 开始画激光，在前60%的等待时间会画出
            Manager.is_await = True
        if self.is_fire:
            # 封印解除，开始发射核弹
            bullet = BossEnemyBullet5(self.screen, player_x, -20)
            self.bullets.add(bullet)
            Boss2.enemy_bullets.add(bullet)
            # 发射一次就行，把fire关了
            self.is_fire = False

    def update(self, player_x=random.randint(50, 430)):  # 玩家死后再发射子弹无法锁定目标，那就随机发射
        self.auto_move()
        self.auto_fire(player_x=player_x)
        self.display()


# 敌机子弹类
class BossEnemyBullet1(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='boss_bullet1.png')
        # 该类子弹可以选择左下/右下之间，随机一个方向进行发射
        self.random_direction = random.randint(0, 2)

    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        if self.random_direction == 0:
            self.rect.left += 1  # 右下
        else:
            self.rect.left -= 1  # 左下
        # 如果子弹移出屏幕下方，则销毁子弹对象
        if self.rect.top > 700:
            self.kill()


class BossEnemyBullet2(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='boss_bullet2.png')
        self.speed = 6


class BossEnemyBullet3(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='boss_bullet3.png')
        self.speed = 4
        self.random_direction = random.randint(0, 2)

    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        if self.random_direction == 0:
            self.rect.left += 1
        else:
            self.rect.left -= 1
        # 如果子弹移出屏幕下方，则销毁子弹对象
        if self.rect.top > 700:
            self.kill()


class BossEnemyBullet4(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='boss_bullet4.png')
        self.speed = 12


class BossEnemyBullet5(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='boss_bullet5.png')
        self.speed = 20


# 背景音乐
class Music(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./music/鲸1.mp3")
        pygame.mixer.music.set_volume(0.5)
        # 此处爆炸音效为私有属性
        self.__bomb = pygame.mixer.Sound('./music/me_down.wav')
        self.__victory = pygame.mixer.Sound('./music/victory.MP3')

    def playBGM(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐

    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)

    def playVictorySound(self):
        pygame.mixer.Sound.play(self.__victory)

    def playBoss2Music(self):
        pygame.mixer.music.load('./music/鲸2.mp3')
        pygame.mixer.music.play(-1)


class GameBG(myclass.GameBackground):
    def __init__(self, screen, bg_size):
        super().__init__(screen, bg_size, path1='bgi4.jpg', path2='bgi5.jpg')


# 管理类，将main()函数变成面向对象编程
class Manager(object):
    bg_size = (480, 700)
    # 创建核弹定时器的id
    create_bullet_id = 10
    # 创建补给定时器的id
    create_supply_id = 6
    # 游戏结束，倒计时的id
    end_id = 15
    # boss形态切换
    is_change = False
    # 激光
    is_await = False
    # 游戏胜利结束
    is_victory = False
    # 游戏失败结束
    is_failure = False
    # 切换时间
    change_time = 5
    # 等待时间
    await_time = 10
    # 倒计时时间
    over_time = 3

    # 飞机生命值
    # hp = 666   # 这个要是全局的话，难怪你第二次玩游戏没命...
    # 得分
    # score = 0  # 也不能全局...

    def __init__(self):
        pygame.init()
        # 创建窗口
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 32)
        # 创建背景图片（静止）
        # self.background = pygame.image.load("./images/background.png")
        # 创建背景图片（动态）
        self.map = GameBG(self.screen, bg_size=Manager.bg_size)
        # 初始化一个装玩家精灵的group
        self.players = pygame.sprite.Group()
        # 初始化一个装敌机精灵的group
        self.enemies = pygame.sprite.Group()
        # 初始化一个装补给精灵的group
        self.supplies = pygame.sprite.Group()
        # 初始化一个玩家爆炸的对象
        self.player_bomb = myclass.Bomb(self.screen, 'me')
        # 初始化两个boss爆炸的对象
        self.boss1_bomb = myclass.Bomb(self.screen, 'boss1')
        self.boss2_bomb = myclass.Bomb(self.screen, 'boss2')
        # 初始化一个声音播放的对象
        self.sound = Music()
        # 飞机生命值
        self.hp = 4200
        self.red = (255, 0, 0)
        self.green = (0, 200, 0)
        self.white = (255, 255, 255)
        # 得分
        # self.score = 0  boss模式没有得分
        # warning闪烁标记
        self.count = 0
        # warning_bg背景图移动
        self.bg_x = 0
        # 飞机战斗力模式
        self.mode = 1
        # 退出游戏标志
        self.exit_game = 0

    def __exit__(self):
        print('退出')
        pygame.quit()
        exit()

    def show_hp(self):
        self.drawText('hp %d' % self.hp, 120, 660, textHeight=14, fontColor=(255, 255, 255))

    def show_bosshp(self):
        self.drawText('hp %d' % self.enemies.sprites()[0].hp, 120, 19, textHeight=14, fontColor=(255, 255, 255))

    def show_laser(self):
        laser = pygame.image.load("./image/laser.png")
        self.screen.blit(laser, (self.players.sprites()[0].rect.centerx - laser.get_rect().width / 2, -25))

    # warning警告条不断左移
    def show_warning_bg(self):
        image_bg = pygame.image.load("./image/warning_bg.png")
        self.screen.blit(image_bg, (self.bg_x, 220))
        self.bg_x -= 1

    def show_warning_icon(self):
        image_bg = pygame.image.load("./image/warning_icon.png")
        self.screen.blit(image_bg, (50, 250))

    def show_change_text(self):
        if 30 <= self.count < 70:
            self.drawText('warning !', 150, Manager.bg_size[1] / 2 - 100,
                          textHeight=50, fontColor=[255, 0, 100])
        elif self.count == 70:
            self.count = 0
        self.count += 1

    def show_victory_text(self):
        # 游戏结束 倒计时后重新开始
        self.drawText('victory %d' % Manager.over_time, 120, Manager.bg_size[1] / 2 - 100,
                      textHeight=50, fontColor=[230, 230, 40])

    def show_over_text(self):
        # 游戏结束 倒计时后重新开始
        self.drawText('gameover %d' % Manager.over_time, 90, Manager.bg_size[1] / 2 - 100,
                      textHeight=50, fontColor=[0, 0, 255])

    def change_timer(self):
        # 倒计时: 不断-1
        Manager.change_time -= 1
        if Manager.change_time == 0:
            # 参数2改为0 定时器停止
            pygame.time.set_timer(Manager.end_id, 0)
            # boss2登场
            self.new_boss2()
            # over_time等参数重置()以免影响后续逻辑
            Manager.change_time = 5
            Manager.is_change = False

    def await_timer(self):
        Manager.await_time -= 1
        if Manager.await_time == 4:  # 将激光图片从屏幕移除
            Manager.is_await = False
        if Manager.await_time == 0:  # 定时器关了
            pygame.time.set_timer(Manager.create_bullet_id, 0)
            # 只有敌机还活着，才能去规定里面的是否发射子弹等行为
            if self.enemies.sprites():
                self.enemies.sprites()[0].timer_flag = False  # 标志定时器此时关闭，下一次激光可用available
                self.enemies.sprites()[0].is_fire = True  # 启动，发射核弹！
                Manager.await_time = 10  # 重置await_time

    def victory_timer(self):
        # 倒计时: 不断-1
        Manager.over_time -= 1
        if Manager.over_time == 0:
            # 参数2改为0 定时器停止
            pygame.time.set_timer(Manager.end_id, 0)
            # 倒计时后退出游戏
            Manager.over_time = 3
            Manager.is_victory = False
            self.exit_game = 1

    def game_over_timer(self):
        # 倒计时: 不断-1
        Manager.over_time -= 1
        if Manager.over_time == 0:
            # 参数2改为0 定时器停止
            pygame.time.set_timer(Manager.end_id, 0)
            # 倒计时后退出游戏
            Manager.over_time = 3
            Manager.is_failure = False
            self.exit_game = 1

    def new_player(self):
        # 创建飞机对象，添加到玩家的组
        player = myclass.Player(self.screen, mode=1)
        self.players.add(player)

    def new_boss1(self):
        # 创建敌机对象，添加到敌机的组
        boss1 = Boss1(self.screen)
        self.enemies.add(boss1)

    def new_boss2(self):
        # 创建敌机对象，添加到敌机的组
        boss2 = Boss2(self.screen)
        self.enemies.add(boss2)

    def new_supply(self):
        # 创建敌机对象，添加到敌机的组
        # 利用随机数，控制隔一段时间才生成补给
        random_num = random.randint(1, 10)
        if random_num == 1:
            supply = myclass.Supply(self.screen, bg_size=Manager.bg_size)
            self.supplies.add(supply)

    # 添加文字
    def drawText(self, text, x, y, textHeight=30, fontColor=(255, 0, 0), backgroundColor=None):
        # 通过字体文件获取字体对象
        font_obj = pygame.font.Font('./font/Genshin default fonts.ttf', textHeight)
        text_obj = font_obj.render(text, True, fontColor, backgroundColor)
        # 获取要显示的对象的rect
        text_rect = text_obj.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = (x, y)
        # 绘制字到指定区域
        self.screen.blit(text_obj, text_rect)

    # 添加血条
    def draw_hp_bar(self, x, y, color=(), width=300, height=15):
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def main(self):
        # 播放音乐
        self.sound.playBGM()
        # 创建一个玩家
        self.new_player()
        # 创建boss1
        self.new_boss1()
        # 创建补给定时器
        pygame.time.set_timer(Manager.create_supply_id, 1000)
        while True:
            if self.exit_game == 1:
                # 有可能定时器还没关掉
                # pygame.time.set_timer(Manager.create_bullet_id, 0)
                # 将Manager.await_time重置，否则下一轮直接负数了...
                Manager.await_time = 10
                Manager.is_await = False
                break
            # 把背景图片贴到窗口(动态: 边移动边重新绘制)
            self.map.move()
            self.map.draw()
            # 绿色血条
            if self.players.sprites():
                self.draw_hp_bar(100, 660, self.green, int(self.hp / 15))
            # 绘制文字hp
            self.show_hp()

            if Manager.is_victory:
                self.show_victory_text()
            elif Manager.is_failure:
                self.show_over_text()
            elif Manager.is_change:
                self.show_warning_bg()
                self.show_warning_icon()
                self.show_change_text()
            elif Manager.is_await:  # 敌机发射核弹前会发射激光预警信号
                self.show_laser()

            # 遍历所有的事件
            # 注意：当type==定时器某个id时，只是那个瞬间定时器开启，所以调用时会每隔一段时间触发一次而已
            # 因此除了在这一瞬间绘制图像文字之外，还要在主循环写一遍绘制
            for event in pygame.event.get():
                # 判断事件类型如果是pygame的退出
                if event.type == QUIT:
                    self.__exit__()
                elif event.type == Manager.create_supply_id:
                    # 创建一个补给
                    self.new_supply()
                elif event.type == Manager.create_bullet_id:
                    # 创建一个激光
                    self.await_timer()
                elif event.type == Manager.end_id:
                    if Manager.is_victory:
                        # 定时器触发的事件
                        self.victory_timer()
                    elif Manager.is_failure:
                        self.game_over_timer()
                    elif Manager.is_change:
                        self.change_timer()
                        print('形态切换定时器')

            # 调用爆炸的对象
            self.player_bomb.draw()
            self.boss1_bomb.draw()
            self.boss2_bomb.draw()

            # 玩家飞机和Boss1子弹的碰撞判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0], Boss1.enemy_bullets, False)
                if is_over:
                    # 判断与之碰撞的子弹类型，进行相应的血量扣除
                    if is_over[0].__class__ == BossEnemyBullet1:
                        self.hp -= 25
                    else:
                        self.hp -= 10
                    is_over[0].kill()
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        Manager.is_failure = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.end_id, 1000)  # 退出游戏倒计时
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 主音乐停止
                        pygame.mixer.music.stop()
            # 玩家飞机和Boss2子弹的碰撞判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0], Boss2.enemy_bullets, True)
                if is_over:
                    # 判断与之碰撞的子弹类型，进行相应的血量扣除
                    if is_over[0].__class__ == BossEnemyBullet3:
                        self.hp -= 35
                    elif is_over[0].__class__ == BossEnemyBullet4:
                        self.hp -= 20
                    else:
                        self.hp -= 200
                    is_over[0].kill()
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        Manager.is_failure = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.end_id, 1000)  # 退出游戏倒计时
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 主音乐停止
                        pygame.mixer.music.stop()

            # 判断玩家飞机和敌机的碰撞
            is_collide = pygame.sprite.groupcollide(self.players, self.enemies, False, False)
            if is_collide:
                self.hp -= 10000  # 玩家飞机直接阵亡
                print('撞机')
                if self.hp <= 0:
                    # hp显示为0而不是负数
                    self.hp = 0
                    Manager.is_failure = True  # 标志游戏结束
                    pygame.time.set_timer(Manager.end_id, 1000)  # 开始下一轮游戏倒计时
                    # 把玩家飞机从精灵组移除
                    self.players.remove(self.players.sprites()[0])
                    items = list(is_collide.items())[0]
                    x = items[0]
                    # 玩家爆炸图片
                    self.player_bomb.action(x.rect)
                    # 爆炸的声音
                    self.sound.playBombSound()
                    # 主音乐停止
                    pygame.mixer.music.stop()

            # 玩家子弹和所有敌机的碰撞判断
            is_enemy = pygame.sprite.groupcollide(myclass.Player.bullets, self.enemies, True, False)
            if is_enemy and list(is_enemy.items())[0][1][0].rect.bottom == 200:  # boss下来后才解除无敌状态，玩家子弹才能生效
                items = list(is_enemy.items())[0]  # 获取第一个键值对: key:子弹  value:敌机列表
                my_bullet = items[0]  # 获取击中boss的子弹
                hit_enemy = items[1][0]  # 获取被击中的敌机对象
                # 根据子弹类型，减少敌机生命值
                if my_bullet.__class__ == myclass.Bullet1:
                    hit_enemy.hp -= 1
                elif my_bullet.__class__ == myclass.Bullet2:
                    hit_enemy.hp -= 3
                elif my_bullet.__class__ == myclass.Bullet3LSlow or my_bullet.__class__ == myclass.Bullet3RSlow \
                        or my_bullet.__class__ == myclass.Bullet3LFast or my_bullet.__class__ == myclass.Bullet3RFast:
                    hit_enemy.hp -= 2
                if hit_enemy.hp <= 0:
                    if hit_enemy.__class__ == Boss1:
                        # boss2音乐
                        self.sound.playBoss2Music()
                        # 加载爆炸动画
                        self.boss1_bomb.action(hit_enemy.rect)
                        # boss形态切换，把boss从精灵组移除
                        hit_enemy.kill()
                        # 定时器6秒后进入第二形态
                        Manager.is_change = True  # 标志过渡信号，绘制warning警告
                        pygame.time.set_timer(Manager.end_id, 1000)  # 倒计时
                    else:
                        # boss2形态被摧毁，游戏胜利
                        # 加载爆炸动画
                        self.boss2_bomb.action(hit_enemy.rect)
                        hit_enemy.kill()
                        Manager.is_victory = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.end_id, 1000)  # 退出游戏倒计时
                        # 胜利的声音
                        self.sound.playVictorySound()
                        # 主音乐停止
                        pygame.mixer.music.stop()

            # 玩家飞机和补给的判断
            if self.players.sprites() and self.supplies.sprites():
                is_supply = pygame.sprite.spritecollide(self.players.sprites()[0], self.supplies, True)
                if is_supply:
                    player = self.players.sprites()[0]
                    print('武器强化！')
                    # 武器模式强化
                    if player.mode < 4:
                        player.mode += 1

            # 玩家飞机和子弹的显示
            self.players.update()
            # 敌机和子弹的显示
            if self.players.sprites() and self.enemies.sprites() and self.enemies.sprites()[0].__class__ == Boss2:
                self.enemies.update(self.players.sprites()[0].rect.centerx)
            else:
                self.enemies.update()
            # 补给的显示
            self.supplies.update()
            # boss血条在最顶图层
            if self.enemies.sprites():
                # boss1阶段绘制两条血条（红色 + 白色）
                if self.enemies.sprites()[0].__class__ == Boss1:
                    self.draw_hp_bar(120, 20, self.red, 240)
                    self.draw_hp_bar(120, 38, self.white, self.enemies.sprites()[0].hp * 3, 8)
                # boss2阶段绘制红色血条
                else:
                    self.draw_hp_bar(120, 20, self.red, self.enemies.sprites()[0].hp / 2)
                self.show_bosshp()
            # 没有赢时，始终显示boss的红色血条
            elif not Manager.is_victory:
                self.draw_hp_bar(120, 20, self.red, 240)

            # 刷新窗口内容
            pygame.display.update()

            time.sleep(0.02)
