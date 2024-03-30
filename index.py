# 首页

import pygame
import sys
import endless
import boss
import history

# 初始化 Pygame
pygame.init()

# 游戏窗口大小
window_size = (480, 700)
screen = pygame.display.set_mode(window_size)
i = 0
index1 = pygame.image.load("./image/index1.png")
index2 = pygame.image.load("./image/index2.png")
index3 = pygame.image.load("./image/index3.png")
# 设置程序标题
pygame.display.set_caption("cyh飞机大战")

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)

# 加载字体
font = pygame.font.Font(None, 36)


class Button:
    def __init__(self, image_path, position, action=None):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.action = action

    def draw(self):
        screen.blit(self.image, self.rect)


# 四张图片按钮
btn1 = Button('./image/无尽模式.png', (160, 375), action='goto_page2')
btn2 = Button('./image/boss模式.png', (160, 450), action='goto_page2')
btn3 = Button('./image/历史记录.png', (160, 525), action='goto_page2')
btn4 = Button('./image/退出游戏.png', (160, 600), action='goto_page2')


class MusicBGM(object):
    def __init__(self):
        self.bgm_playing = False
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.set_volume(0.5)

    def playMyBGM(self):
        pygame.mixer.music.load("./music/1.4入场.mp3")
        pygame.mixer.music.play(-1)  # 开始播放音乐, -1表示循环播放
        self.bgm_playing = True

    def stopBGM(self):
        pygame.mixer.music.stop()
        self.bgm_playing = False

    def is_playing(self):
        return self.bgm_playing
def main_endless():
    manager = endless.Manager()
    manager.main()
def main_boss():
    manager = boss.Manager()
    manager.main()
def main_histroy():
    manager = history.Manager()
    manager.main()

music1 = MusicBGM()
music1.playMyBGM()
# 游戏主循环
while True:
    # 检查音乐是否在播放，如果不在，重新播放
    if not music1.is_playing():
        music1.playMyBGM()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查按钮点击事件
            if btn1.rect.collidepoint(event.pos):
                print("无尽模式")
                # 主页面背景音乐关了
                music1.bgm_playing = False
                # 在这里添加开始游戏的逻辑——无尽模式
                main_endless()
            elif btn2.rect.collidepoint(event.pos):
                print("boss模式")
                # 主页面背景音乐关了
                music1.bgm_playing = False
                # 在这里添加开始游戏的逻辑——boss模式
                main_boss()
            elif btn3.rect.collidepoint(event.pos):
                print("历史分数")
                # 主页面背景音乐不用关，只是查个记录而已
                # music1.bgm_playing = False
                main_histroy()
                # handle_button_click(btn3.action)
            elif btn4.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    # 渲染背景（3张背景图动态切换）
    i += 1
    if i == 1:
        screen.blit(index1, (0, 0))
    elif i == 3:
        screen.blit(index2, (0, 0))
    elif i == 5:
        screen.blit(index3, (0, 0))
    elif i == 7:
        screen.blit(index2, (0, 0))
        i = 0

    # 绘制按钮
    btn1.draw()
    btn2.draw()
    btn3.draw()
    btn4.draw()

    # 更新屏幕
    pygame.display.flip()
