# 无尽模式优化
# 新增补给功能，得到补给后强化武器，增加弹道，增加敌机和子弹种类等

import pygame
import time
import random
import myclass
from pygame.locals import *  # 不引入变量，只引入常量，防止命名冲突
from datetime import datetime
from mysql_tool import MysqlTool

# 全局变量，最高得分（需要从数据库里面查询获取，并在游戏中可能动态更新）
# 连接 MySQL 数据库
with MysqlTool() as db:
    # 执行查询数据库字段的SQL语句
    rows = db.execute('SELECT * FROM score_table')
# 遍历所有行的分数列，找出最高分
highest_score = 0
for i, row in enumerate(rows):
    if row[1] > highest_score:
        highest_score = row[1]


# 继承Enemy父类，共4个敌机子类，需重写父类方法
class MiniEnemy(myclass.Enemy):
    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=1, speed=4, path="mini_enemy.png", bg_size=(480, 700))

    def auto_fire(self):
        random_num = random.randint(1, 40)
        if random_num == 1:
            bullet = MiniEnemyBullet(self.screen, self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            MiniEnemy.enemy_bullets.add(bullet)


class SmallEnemy(myclass.Enemy):
    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=2, speed=3, path="small_enemy.png", bg_size=(480, 700))

    def auto_fire(self):
        random_num = random.randint(1, 40)
        if random_num == 1:
            bullet = SmallEnemyBullet(self.screen, self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            SmallEnemy.enemy_bullets.add(bullet)


class MidEnemy(myclass.Enemy):
    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=3, speed=2, path="mid_enemy.png", bg_size=(480, 700))

    def auto_fire(self):
        random_num = random.randint(1, 40)
        if random_num == 1:
            bullet = MidEnemyBullet(self.screen, self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            MidEnemy.enemy_bullets.add(bullet)


class BigEnemy(myclass.Enemy):
    def __init__(self, screen):
        # 在子类的init初始化中，调用父类的构造函数，并传参进行初始化
        super().__init__(screen, hp=10, speed=1, path="big_enemy.png", bg_size=(480, 700))

    def auto_fire(self):
        random_num = random.randint(1, 40)
        if random_num == 1:
            bullet = BigEnemyBullet(self.screen, self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet)
            # 把子弹添加到类属性的子弹组里
            BigEnemy.enemy_bullets.add(bullet)


# 四种敌机对应四种子弹，需继承并重写父类EnemyBullet的属性和方法
class MiniEnemyBullet(myclass.EnemyBullet):
    # 外部创建对象需要传3个参：screen, x, y
    def __init__(self, screen, x, y):
        # 重写父类方法时，根据子类的类型选择正确的图片初始化(不用外部传参)
        super().__init__(screen, x, y, path='mini_bullet.png')
        self.speed = 5


class SmallEnemyBullet(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='small_bullet.png')
        self.speed = 6


class MidEnemyBullet(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='mid_bullet.png')
        self.speed = 6


class BigEnemyBullet(myclass.EnemyBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, path='big_bullet.png')
        self.speed = 7


# 背景音乐
class Music(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./music/1.4厅.mp3")
        pygame.mixer.music.set_volume(0.5)
        # 此处爆炸音效为私有属性
        self.__bomb = pygame.mixer.Sound('./music/me_down.wav')

    def playBGM(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐

    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)


# 背景类子类，需要传入所需的具体背景图片
class GameBG(myclass.GameBackground):
    def __init__(self, screen, bg_size):
        super().__init__(screen, bg_size, path1='bgi1.jpg', path2='bgi2.jpg')


# 管理类，将main()函数变成面向对象编程
class Manager(object):
    bg_size = (480, 700)
    # 创建敌机定时器的id  (id随便设置，不同定时器的id不要重复就行)
    create_enemy_id = 10
    # 创建补给定时器的id
    create_supply_id = 6
    # 游戏结束，倒计时的id
    game_over_id = 11

    # 飞机生命值
    # hp = 666   # 不能全局，否则会影响下一局游戏的生命值
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
        # 初始化多个敌机爆炸的对象
        self.mini_enemy_bomb = myclass.Bomb(self.screen, 'mini_enemy')
        self.small_enemy_bomb = myclass.Bomb(self.screen, 'small_enemy')
        self.mid_enemy_bomb = myclass.Bomb(self.screen, 'mid_enemy')
        self.big_enemy_bomb = myclass.Bomb(self.screen, 'big_enemy')
        # 初始化一个声音播放的对象
        self.sound = Music()
        # 绿色
        self.green = (0, 200, 0)
        # 飞机生命值
        self.hp = 560
        # 得分
        self.score = 0
        # 倒计时时间
        self.over_time = 3
        # 游戏是否结束
        self.is_game_over = False
        # 退出游戏标志
        self.exit_game = 0
        # 补给持续时间
        self.supply_collected_time = 0

    def __exit__(self):
        print('退出')
        pygame.quit()
        exit()

    def show_hp(self):
        self.drawText('hp %d' % self.hp, 120, 660, textHeight=16, fontColor=(255, 255, 255))

    def show_score(self):
        self.drawText('score %d' % self.score, 20, 10, textHeight=18, fontColor=(255, 255, 255))

    # 更新最高分
    def show_highscore(self):
        # 添加global关键字，否则Python将会创建一个新的局部变量而不是修改全局变量
        global highest_score
        # 当前分数和数据库历史最高分比较，取较大值作为当前最高分
        highest_score = max(highest_score, self.score)
        self.drawText('highest %d' % highest_score, 20, 40, textHeight=18, fontColor=(255, 255, 255))

    def show_over_text(self):
        # 游戏结束 倒计时后重新开始
        self.drawText('gameover %d' % self.over_time, 90, Manager.bg_size[1] / 2,
                      textHeight=50, fontColor=[0, 0, 255])

    def game_over_timer(self):
        self.show_over_text()
        # 倒计时: 不断-1
        self.over_time -= 1
        if self.over_time == 0:
            # 参数2改为0 定时器停止
            pygame.time.set_timer(Manager.game_over_id, 0)
            # 更新最高分
            with MysqlTool() as db:
                # 插入本次游戏数据(分成 sql语句 + args参数 两部分)
                current_datetime = datetime.now()
                sql2 = f"INSERT INTO score_table (SCORE, DATE) VALUES (%s, %s)"
                args = (self.score, f'{current_datetime}')
                db.execute(sql2, args, commit=True)
            self.exit_game = 1

            # 有些类属性要清空（静态方法清空）
            MiniEnemy.clear_bullets()
            SmallEnemy.clear_bullets()
            MidEnemy.clear_bullets()
            BigEnemy.clear_bullets()
            myclass.Player.clear_bullets()

    def new_player(self):
        # 创建飞机对象，添加到玩家的组
        player = myclass.Player(self.screen, mode=0)
        self.players.add(player)

    def new_enemy(self):
        # 创建敌机对象，添加到敌机的组
        # 利用随机数，生成随机的敌机，级别越小的敌机，出现概率越大
        random_num = random.randint(1, 20)
        if random_num in [1, 2]:
            big = BigEnemy(self.screen)
            self.enemies.add(big)
        elif random_num in [3, 4, 5]:
            mid = MidEnemy(self.screen)
            self.enemies.add(mid)
        elif random_num in [6, 7, 8, 9, 10]:
            small = SmallEnemy(self.screen)
            self.enemies.add(small)
        else:
            mini = MiniEnemy(self.screen)
            self.enemies.add(mini)

    def new_supply(self):
        # 创建敌机对象，添加到敌机的组
        # 利用随机数，控制隔一段时间才生成补给
        random_num = random.randint(1, 20)
        if random_num == 8:
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

    # 画血条
    def draw_hp_bar(self, x, y, color=(), width=300, height=20):
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def main(self):
        # 播放音乐
        self.sound.playBGM()
        # 创建一个玩家
        self.new_player()
        # 创建敌机定时器
        pygame.time.set_timer(Manager.create_enemy_id, 1000)
        # 创建补给定时器
        pygame.time.set_timer(Manager.create_supply_id, 1000)

        while True:
            if self.exit_game == 1:
                break
            # 把背景图片贴到窗口(静止)
            # self.screen.blit(self.background, (0, 0))
            # 把背景图片贴到窗口(动态: 边移动边重新绘制)
            self.map.move()
            self.map.draw()
            # 绿色血条
            if self.players.sprites():
                self.draw_hp_bar(100, 660, self.green, int(self.hp / 2))
            # 绘制文字hp
            self.show_hp()
            # 绘制得分
            self.show_score()
            # 绘制最高分
            self.show_highscore()

            if self.is_game_over:
                # 判断游戏结束才显示结束文字
                self.show_over_text()

            # 遍历所有的事件，每隔millis个时间单位就会触发一次定时器id生效，这里是捕获当次循环时定时器触发的所有事件并执行相关函数
            for event in pygame.event.get():
                # 判断事件类型如果是pygame的退出
                if event.type == QUIT:
                    self.__exit__()
                elif event.type == Manager.create_enemy_id:
                    # 创建一个敌机(不等概率的随机，共四种敌机随机创建一种)
                    self.new_enemy()
                elif event.type == Manager.create_supply_id:
                    # 创建一个补给（大概20秒一个）
                    self.new_supply()
                elif event.type == Manager.game_over_id:
                    # 定时器触发的事件：游戏结束
                    self.game_over_timer()

            # 调用爆炸的对象
            self.player_bomb.draw()
            self.mini_enemy_bomb.draw()
            self.small_enemy_bomb.draw()
            self.mid_enemy_bomb.draw()
            self.big_enemy_bomb.draw()

            # 玩家飞机和mini敌机子弹的判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0],
                                                      MiniEnemy.enemy_bullets, True)
                if is_over:
                    self.hp -= 2
                    print('被mini击中，hp-2')
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        self.is_game_over = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.game_over_id, 1000)
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 更新最高分
                        self.show_highscore()
                        pygame.mixer.music.stop()

            # 玩家飞机和小敌机子弹的判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0],
                                                      SmallEnemy.enemy_bullets, True)
                if is_over:
                    self.hp -= 5
                    print('小中弹hp-5')
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        self.is_game_over = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.game_over_id, 1000)  # 开始下一轮游戏倒计时
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 更新最高分
                        self.show_highscore()
                        pygame.mixer.music.stop()

            # 玩家飞机和中敌机子弹的判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0],
                                                      MidEnemy.enemy_bullets, True)
                if is_over:
                    self.hp -= 10
                    print('中中弹hp-10')
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        self.is_game_over = True  # 标志游戏结束，画对应提示文字
                        pygame.time.set_timer(Manager.game_over_id, 1000)  # 开始下一轮游戏倒计时
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 更新最高分
                        self.show_highscore()
                        pygame.mixer.music.stop()

            # 玩家飞机和大敌机子弹的判断
            if self.players.sprites():
                is_over = pygame.sprite.spritecollide(self.players.sprites()[0],
                                                      BigEnemy.enemy_bullets, True)
                if is_over:
                    print(vars(self.players.sprites()[0]))
                    print(vars(BigEnemy.enemy_bullets))
                    dir(self.players.sprites()[0])
                    dir(BigEnemy.enemy_bullets)
                    self.hp -= 20
                    print('大中弹hp-20')
                    if self.hp <= 0:
                        # hp显示为0而不是负数
                        self.hp = 0
                        self.is_game_over = True  # 标志游戏结束
                        pygame.time.set_timer(Manager.game_over_id, 1000)  # 结束倒计时
                        # 爆炸动画
                        self.player_bomb.action(self.players.sprites()[0].rect)
                        # 把玩家飞机从精灵组移除
                        self.players.remove(self.players.sprites()[0])
                        # 爆炸的声音
                        self.sound.playBombSound()
                        # 更新最高分
                        self.show_highscore()
                        pygame.mixer.music.stop()

            # 判断玩家飞机和敌机的碰撞
            is_collide = pygame.sprite.groupcollide(self.players, self.enemies, False, True)
            if is_collide:
                # is_collide.items() 是键值对列表，每个元素都是 玩家飞机 + 敌机列表 的键值对
                hit_enemy = list(is_collide.items())[0][1][0]  # 碰撞的第一个敌机
                if hit_enemy.__class__ == MiniEnemy:
                    self.hp -= 30
                elif hit_enemy.__class__ == SmallEnemy:
                    self.hp -= 60
                elif hit_enemy.__class__ == MidEnemy:
                    self.hp -= 100
                else:
                    self.hp -= 200
                print('撞机')
                if self.hp <= 0:
                    # hp显示为0而不是负数
                    self.hp = 0
                    # 把玩家飞机从精灵组移除
                    self.players.remove(self.players.sprites()[0])
                    self.is_game_over = True  # 标志游戏结束
                    pygame.time.set_timer(Manager.game_over_id, 1000)  # 开始游戏倒计时
                    items = list(is_collide.items())[0]
                    print(items)  # 键是玩家飞机对象，值是与之碰撞的小敌机对象的列表
                    x = items[0]
                    y = items[1][0]  # 碰撞的第一个敌机
                    # 玩家爆炸图片
                    self.player_bomb.action(x.rect)
                    # 敌机爆炸图片
                    if hit_enemy.__class__ == MiniEnemy:
                        self.mini_enemy_bomb.action(y.rect)
                    elif hit_enemy.__class__ == SmallEnemy:
                        self.small_enemy_bomb.action(y.rect)
                    elif hit_enemy.__class__ == MidEnemy:
                        self.mid_enemy_bomb.action(y.rect)
                    else:
                        self.big_enemy_bomb.action(y.rect)
                    # 爆炸的声音
                    self.sound.playBombSound()
                    # 更新最高分
                    self.show_highscore()
                    pygame.mixer.music.stop()

            # 玩家子弹和所有敌机的碰撞判断
            is_enemy = pygame.sprite.groupcollide(myclass.Player.bullets, self.enemies, True, False)
            if is_enemy:
                items = list(is_enemy.items())[0]  # 获取第一个键值对: key:子弹  value:敌机列表
                hit_enemy = items[1][0]  # 获取被击中的敌机对象
                print(hit_enemy)
                # 敌机生命值-1
                hit_enemy.hp -= 1  # 减少敌机生命值
                if hit_enemy.hp <= 0:
                    # 根据击落的敌机类型进行 爆炸、加分
                    if hit_enemy.__class__ == MiniEnemy:
                        # 分数增加
                        self.score += 10
                        # 敌机爆炸图片
                        self.mini_enemy_bomb.action(hit_enemy.rect)
                    elif hit_enemy.__class__ == SmallEnemy:
                        self.score += 20
                        self.small_enemy_bomb.action(hit_enemy.rect)
                    elif hit_enemy.__class__ == MidEnemy:
                        self.score += 40
                        self.mid_enemy_bomb.action(hit_enemy.rect)
                    else:
                        self.score += 100
                        self.big_enemy_bomb.action(hit_enemy.rect)
                    # 如果生命值小于等于0，敌机死亡，从屏幕上消失
                    hit_enemy.kill()  # 销毁对象，释放内存
                    # self.enemies.remove(hit_enemy)  # 移除但不释放内存
                    # 爆炸的声音
                    self.sound.playBombSound()

            # 玩家飞机和补给的判断
            if self.players.sprites() and self.supplies.sprites():
                is_supply = pygame.sprite.spritecollide(self.players.sprites()[0], self.supplies, True)
                if is_supply:
                    player = self.players.sprites()[0]
                    print('武器强化！')
                    # 记录补给获取的时间
                    player.supply_collected_time = time.time()

            # 玩家飞机和子弹的显示
            self.players.update()
            # 敌机和子弹的显示
            self.enemies.update()
            # 补给的显示
            self.supplies.update()
            # 刷新窗口内容
            pygame.display.update()
            time.sleep(0.02)
