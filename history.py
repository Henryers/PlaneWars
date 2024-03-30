# 无尽模式分数历史记录

import pygame
import sys
from mysql_tool import MysqlTool

pygame.init()


class Button:
    def __init__(self, image_path, position, action=None):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.action = action

    def draw(self):
        screen.blit(self.image, self.rect)


screen = pygame.display.set_mode((480, 700))
pygame.display.set_caption('MySQL 数据库字段显示')
btn5 = Button('./image/返回.png', (50, 50), action='goto_page1')

black = (0, 0, 0)
white = (255, 255, 255)
blue = (100, 220, 255)


class Manager(object):
    def __init__(self):
        self.exit = 0
        self.highest_score = 0

    def drawText(self, text, x, y, textHeight=30, fontColor=(255, 0, 0), backgroundColor=None):
        # 通过字体文件获取字体对象
        font_obj = pygame.font.Font('./font/Genshin default fonts.ttf', textHeight)
        text_obj = font_obj.render(text, True, fontColor, backgroundColor)
        # 获取要显示的对象的rect
        text_rect = text_obj.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = (x, y)
        # 绘制字到指定区域
        screen.blit(text_obj, text_rect)

    def main(self):
        # 先把背景和返回键画了再说
        bg_image = pygame.image.load('./image/bgi3.jpg')
        screen.blit(bg_image, (0, 0))
        btn5.draw()
        # 连接 MySQL 数据库（使用with能确保在使用完毕后自动关闭游标和连接，以免忘记手动关闭）
        with MysqlTool() as db:
            # 执行查询数据库字段的SQL语句
            rows = db.execute('SELECT * FROM score_table')

        while True:
            if self.exit == 1:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 退出程序之前做一些pygame的清理工作
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn5.rect.collidepoint(event.pos):
                        print("返回")
                        self.exit = 1
                        break

            # 在 Pygame 窗口上显示数据库表数据（逆序并打印最后5行）
            row_height = 40
            num_rows_to_print = min(len(rows), 5)  # 控制打印的行数，取前5行或实际行数的较小值

            # 遍历所有行的分数列，找出最高分
            for i, row in enumerate(rows):
                if row[1] > self.highest_score:  # 该行数据的第二个元素[1]记录着分数
                    self.highest_score = row[1]
            # 逆序并取最后5行
            for i, row in enumerate(reversed(rows[-num_rows_to_print:])):   # -5到-1 末尾5行
                for j, value in enumerate(row[1:]):   # 遍历后两列，j = 0/1
                    self.drawText(str(value), 80 + j * 100, 250 + i * row_height, 20, blue)

            # 先渲染，再在指定位置画出文本
            self.drawText('score            time', 80, 150, 25, blue)
            self.drawText('highest score:{}'.format(self.highest_score), 120, 550, 25, blue)
            pygame.display.flip()
