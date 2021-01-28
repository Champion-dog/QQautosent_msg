# -*- coding: UTF-8 -*-
# @Email  :youclark00@gmail.com
# @Author :YouTian
import win32clipboard as cb
from io import BytesIO
from PIL import Image
import win32gui
import win32con
import threading


class QqAutoSent(object):

    def __init__(self, who, msg, pathfile, mode):               # 初始化
        self.who = who                                          # 要发送信息的好友名称
        self.msg = msg                                          # 文本信息
        self.pathfile = pathfile                                # 要发送的图片路径
        self.mode = mode                                        # 确定是发送文本还是图片

    def setPic(self):
        """
        将要发送的图片放置到剪切板上
        :return: none
        """
        img = Image.open(self.pathfile)
        output = BytesIO()
        img.convert("RGB").save(output, "BMP")                  # 保存成BMP形式
        data = output.getvalue()[14:]                           # bmp文件头14个字节丢弃
        output.close()
        cb.OpenClipboard()                                      # 打开剪贴板
        cb.EmptyClipboard()                                     # 清空剪贴板
        cb.SetClipboardData(win32con.CF_DIB, data)              # 将图片放置到剪贴板
        cb.CloseClipboard()                                     # 关闭剪贴板

    def setText(self):
        """
        将要发送的文本放置到剪切板上
        :return: none
        """
        cb.OpenClipboard()
        cb.EmptyClipboard()
        cb.SetClipboardData(win32con.CF_UNICODETEXT, self.msg)  # 将文本放置到剪贴板
        cb.CloseClipboard()

    def send_content(self):
        """
        mode: 发送内容的形式
        :return: none
        """
        # 将消息写到剪贴板
        if self.mode == "picture":                              # 发送图片
            self.setPic()
        else:                                                   # 发送文本
            self.setText()
        qq = win32gui.FindWindow("TXGuiFoundation", self.who)   # 通过spy++等软件，获取窗口信息
        win32gui.SendMessage(qq, 258, 22, 2080193)
        win32gui.SendMessage(qq, 770, 0, 0)

        win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


if __name__ == '__main__':
    pic_file = r'C:\Users\lenovo\Desktop\temper.jpg'
    msg = 'hello world！'
    who = "王二狗"

    pic = QqAutoSent(who, None, pic_file, "picture")            # 实例化发送图片的类
    text = QqAutoSent(who, msg, pic_file, "text")               # 实例化发送文本的类

    t1 = threading.Thread(target=pic.send_content())            # 发送图片的线程
    t2 = threading.Thread(target=text.send_content())           # 发送文本的线程
