#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time  : 2019/7/12 0012 0:17
# @File  : progress_bar.py
# @email : spirit_az@foxmail.com
__author__ = 'ChenLiang.Miao'

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# import --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os
import glob
import random
import pg_conf
import existUI as exUI
import baseFunction as bFc

# proc function -+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# get dirname
thisFolder = bFc.getScriptPath()


# function main -+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def icon_path(in_name):
    """
    get icons path
    :param in_name:
    :return: str
    """
    return os.path.join(thisFolder, 'icons', in_name).replace('\\', '/')


def get_gif():
    """
    get gif path
    :return:  str
    """
    bg_path = os.path.join(thisFolder, 'icons/update_gif/*.gif').replace('\\', '/')
    lists = glob.glob(bg_path)
    num = random.randrange(len(lists))
    return os.path.normpath(lists[num]).replace('\\', '/')


class progress_bar(exUI.QDialog):
    """
    A progress bar
    example :

    import pg_conf
    import progress_bar

    '''
    args[0] = UI name
    args[1] = parent_UI
    args[2] = function
    '''
    connect(partial(progress_bar.show, *args, **kwargs))

    function(*args, **kwargs):
        '''
        parameter
        '''
        pg_conf.progress_current_val = 0
        pg_conf.progress_max_val = 100
        pg_conf.progress_win_t = ''
        pg_conf.progress_title = ''
        pg_conf.progress_label = ""
        for i in range(101):
            time.sleep(0.3)
            pg_conf.progress_current_val = i
            pg_conf.progress_label = "Had Finished {}%!!".format(i)

    ~show()
    ~~partial(progress_bar.show, "txt_", None, self.txt_pro)

    """
    pos_x = 500
    offset_y = 200

    def __init__(self, obj_name, parent=None):
        """
        create UI
        :param obj_name:
        :param parent:
        """
        super(progress_bar, self).__init__(parent)
        # 设置 可移动
        self.setMouseTracking(True)
        # 设置 窗口透明
        self.setAttribute(exUI.Qt.WA_TranslucentBackground, 1)
        self.setWindowFlags(exUI.Qt.FramelessWindowHint | exUI.Qt.WindowStaysOnTopHint)
        # 设置 窗口名称
        # exUI.Raise(obj_name)
        #
        self.setObjectName(obj_name)
        self.setWindowTitle(obj_name)

        self.ver_lay = exUI.QVBoxLayout(self)

        gif_path = get_gif()
        self.movie = exUI.QMovie(gif_path)
        self.setFixedWidth(self.pos_x)

        font = exUI.QFont()
        font.setPointSize(20)

        self.label_movie_size = exUI.QLabel(self)
        self.label_movie = exUI.QLabel(self)
        self.ver_lay.addWidget(self.label_movie_size)
        self.label_movie_size.setMovie(self.movie)
        self.label_movie_size.setMaximumWidth(0)

        self.label_title = exUI.QLabel(self)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet('QLabel{color: rgb(180, 20, 16);}')
        self.ver_lay.addWidget(self.label_title)

        self.progress = exUI.QProgressBar(self)
        self.progress.setMinimum(0)

        qss_pro = """QProgressBar{
                border: none;
                color: white;
                text-align: center;
                background: rgb(68, 69, 73);
                }
                QProgressBar::chunk {
                        border: none;
                        background: rgb(90, 150, 60);
                }"""

        self.progress.setStyleSheet(qss_pro)
        self.ver_lay.addWidget(self.progress)

        self.label_message = exUI.QLabel(self)
        self.label_message.setFont(font)
        self.label_message.setStyleSheet('QLabel{color: rgb(0, 100, 200);}')

        self.ver_lay.addWidget(self.label_message)

        spacerItem = exUI.QSpacerItem(20, 40, exUI.QSizePolicy.Minimum, exUI.QSizePolicy.Expanding)
        self.ver_lay.addItem(spacerItem)

        self.bt_clicked()

    def __init__UI__(self):
        """
        初始化UI面板
        :return:
        """
        pass

    def bt_clicked(self):
        """
        所有的按钮信号槽链接
        :return:
        """
        self.movie.frameChanged.connect(self.on_next)
        pass

    # +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
    def on_next(self):
        """
        frame key
        :return:
        """
        pixmap = self.movie.currentPixmap()
        self.label_movie.setPixmap(pixmap)

        of_x, of_y = pixmap.width(), pixmap.height()

        progress_title = pg_conf.progress_title
        progress_label = pg_conf.progress_label
        progress_current_val = pg_conf.progress_current_val
        progress_max_val = pg_conf.progress_max_val

        self.progress.setMaximum(progress_max_val)
        self.progress.setValue(progress_current_val)
        self.label_title.setText(progress_title)
        self.label_message.setText(progress_label)

        offset = progress_current_val * 1.00 / progress_max_val * (self.pos_x + of_x)
        self.label_movie.setGeometry(self.pos_x - offset, 10, of_x, of_y)

    # +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
    def mousePressEvent(self, event):
        if event.buttons() == exUI.Qt.LeftButton:
            self.c_pos = event.globalPos() - self.pos()
            self.m_pressed = True

    def mouseMoveEvent(self, event):
        if event.buttons() == exUI.Qt.LeftButton:
            if self.m_pressed:
                self.move(event.globalPos() - self.c_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_pressed = False

    # def resizeEvent(self, event):
    #     self.setAttribute(Qt.WA_TranslucentBackground, 1)

    def showEvent(self, *args):
        self.movie.start()
        s_size = self.size()
        self.setFixedSize(s_size)
        pixmap = self.movie.currentPixmap()

        self.label_title.setGeometry(10, pixmap.height() + 10, self.pos_x, 50)
        self.progress.setGeometry(10, pixmap.height() + 60, self.pos_x, 10)
        self.label_message.setGeometry(10, pixmap.height() + 80, self.pos_x, 50)

        self.setFixedHeight(pixmap.height() + self.offset_y)
        p_ui = self.parent()
        if p_ui:
            width, height = p_ui.width() - s_size.width(), p_ui.height() - s_size.height()
            self.move(width / 2, height / 2)

    def accept(self):
        self.movie.stop()
        self.movie.deleteLater()
        super(progress_bar, self).accept()

    def reject(self):
        if pg_conf.progress_func_conf:
            self.movie.stop()
            # self.movie.deleteLater()
            exUI.deleteUI(self.movie.objectName())
            super(progress_bar, self).reject()


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

class m_thread(exUI.QThread):
    def __init__(self, func, UI_object, parent_UI, *args, **kwargs):
        super(m_thread, self).__init__(parent_UI)
        self.func = func
        self.UI_object = UI_object
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        pg_conf.progress_func_conf = True
        exUI.deleteUI(self.UI_object.objectName())


def show(*args, **kwargs):
    obj_name, parent_UI, func = args[0], args[1], args[2]
    args = args[3:]
    dlg = progress_bar(obj_name, parent=parent_UI)
    if hasattr(func, "__call__"):
        mayaWindow = exUI.GetMayaMainWindow()
        pg_conf.progress_thread = m_thread(func, dlg, mayaWindow, *args, **kwargs)
        pg_conf.progress_thread.start()
    else:
        pg_conf.progress_func_conf = True
        exUI.deleteUI(dlg.objectName())
    dlg.exec_()
    return
