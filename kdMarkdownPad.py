#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import markdown
import time
from PyQt5.QtCore import pyqtSlot, QFile,QEvent
from PyQt5.Qt import QCursor

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QWidget,
    QMainWindow,
    QApplication,
    QFileDialog,
    QTextBrowser,
    QMenu,
    QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtGui
import kdconfig
import kdMarkdownPad_rc
import listActionHandler

class kdMarkdownPad(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kdMarkdownPad.ui", self)

        self.fmt='%Y-%m-%d %H:%M:%S'

        # ~ 1未保存,2是已保存
        self.state = 2
        # ~ 改变五次自动预览
        self.autopreview_change_counter = 0
        self.autosave_change_counter = 0
        self.handbook = QWebEngineView()

        # ~ 加载最近打开的文件
        self.conf = kdconfig.init_conf()
        self.cur_file = None
        if self.conf:
            self.cur_file = self.conf["cur_file"]
            with open(self.cur_file) as f:
                self.te_editor.setPlainText(f.read())
                self.state = 2
            self.statusbar.showMessage(self.cur_file)
        self.cursor = self.te_editor.textCursor()
        # ~ self.listWidgetHandler = listWidgetHandler()
        # ~ self.pb_heading.customContextMenuRequested.connect(self.mpb_heading)
        self.popMenu = QMenu()
        self.pb_heading.installEventFilter(self)
        self.pb_bold.installEventFilter(self)
        self.pb_unsort_list.installEventFilter(self)
        # ~ self.popMenu.installEventFilter(self)

    def now(self):
        return time.strftime(self.fmt,time.localtime(time.time()))     #把传入的元组按照格式，输出字符串


    @pyqtSlot()
    def on_te_editor_textChanged(self):
        self.state = 1
        self.autopreview_change_counter += 1
        self.autosave_change_counter += 1
        if self.autopreview_change_counter >= int(self.le_autopreview_after_change.text()):
            self.on_pb_preview_clicked()
            self.autopreview_change_counter = 0

        if self.autosave_change_counter > int(self.le_autosave_after_change.text()):
            self.on_pb_save_file_clicked()

    @pyqtSlot()
    def on_pb_new_file_clicked(self):
        if self.state == 1:
            reply = QMessageBox.information(
                self, "文件尚未保存", "是否保存?", QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.on_pb_save_clicked()

        self.cur_file = None
        self.te_editor.clear()
        self.state = 2
        self.statusbar.clearMessage()

    @pyqtSlot()
    def on_pb_preview_clicked(self):
        html = markdown.markdown(self.te_editor.toPlainText())
        self.tb_viewer.setHtml(html)
        self.tb_viewer.moveCursor(self.tb_viewer.textCursor().End)

    @pyqtSlot()
    def on_pb_open_file_clicked(self):
        self.get_cur_path()
        file_path = QFileDialog.getOpenFileName(
            None, "open file", self.cur_file, "*.md"
        )

        if file_path[0] == "":
            return
        self.cur_file = file_path[0]
        with open(self.cur_file, "r") as f:
            my_txt = f.read()
            self.autopreview_change_counter = 5
            self.te_editor.setPlainText(my_txt)
            self.state = 2
        kdconfig.update_conf(self.cur_file)

    @pyqtSlot()
    def on_pb_save_file_clicked(self):
        # ~ 获取路径
        if self.cur_file is None:
            path = os.path.dirname(self.conf["cur_file"])
            file_path = QFileDialog.getSaveFileName(self, "save file", path)
            if file_path[0] == "":
                return
            self.cur_file = file_path[0]

        # ~ 保存文件
        with open(self.cur_file, "w") as f:
            f.write(self.te_editor.toPlainText())
            self.state = 2
            self.statusbar.showMessage("保存文件成功," + self.cur_file +"," str(self.now()))
        kdconfig.update_conf(self.cur_file)

    @pyqtSlot()
    def on_pb_handbook_clicked(self):
        with open(sys.path[0] + "/markdown语法.md", "r") as f:
            html = markdown.markdown(f.read())
            self.handbook.setHtml(html)
            self.handbook.show()

    def get_cur_path(self):
        if self.cur_file is None:
            return os.path.dirname(self.conf["cur_file"])
        else:
            return os.path.dirname(self.cur_file)

    # ~ @pyqtSlot()
    # ~ def on_pb_bold_clicked(self):
        # ~ cursor = self.te_editor.textCursor()
        # ~ print(cursor.anchor(),cursor.position())
        # ~ anchor = cursor.anchor()
        # ~ position = cursor.position()
        # ~ selected_text_length = len(cursor.selectedText())
        # ~ cursor.clearSelection()
        # ~ cursor.setPosition(anchor)
        # ~ cursor.insertText("** ")
        # ~ cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor,selected_text_length)
        # ~ cursor.setPosition(position + selected_text_length + 3)
        # ~ cursor.insertText(" **")

        # ~ print("selected"+ self.te_editor.placeholderText())
        # ~ self.te_editor.setTextCursor(cursor)


    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        print(qtype)
        action = None
        if qtype == QEvent.HoverEnter:
            if qobject == self.pb_bold:
                action = self.popMenu.exec_(listActionHandler.bold,QCursor.pos())
            elif qobject ==  self.pb_heading:
                action = self.popMenu.exec_(listActionHandler.headdings,QCursor.pos())
            elif qobject == self.pb_unsort_list:
                action = self.popMenu.exec_(listActionHandler.unsort_lists,QCursor.pos())
            if action:
                print(action.text())
                listActionHandler.handle_action(action,self.te_editor.textCursor())
        # ~ elif qtype == QEvent.Leave:
        else:
            pass
            # ~ print("leave")
            # ~ self.popMenu.close()
        return False
        # ~ if qtype == QEvent.HoverLeave:
            # ~ print("HoverLeave")
            # ~ return True
        # ~ elif qtype == QEvent.HoverEnter:
            # ~ print("HoverEnter")
            # ~ print(qevent.pos())
            # ~ return True
        # ~ else:
            # ~ return False
           # ~ ... hover logic depending in which qobject, since you have 10 buttons
        # ~ return super(MyWidget, self).eventFilter(qobject, qevent)

    @pyqtSlot()
    def on_pb_bold_and_underline_clicked(self):
        listActionHandler.add_before_and_after(self.te_editor.textCursor(),"*** "," ***")

    @pyqtSlot()
    def on_pb_delete_line_clicked(self):
        listActionHandler.add_before_and_after(self.te_editor.textCursor(),"~~ "," ~~")

    @pyqtSlot()
    def on_pb_quote_clicked(self):
        listActionHandler.add_start("> ",self.te_editor.textCursor())

    @pyqtSlot()
    def on_pb_hr_clicked(self):
        cursor = self.te_editor.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Down)
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.insertText(" ---\n")
        cursor.movePosition(QtGui.QTextCursor.Down)
        self.te_editor.setTextCursor(cursor)
    @pyqtSlot()
    def on_pb_italic_clicked(self):
        listActionHandler.add_before_and_after(self.te_editor.textCursor(),"* "," *")
    @pyqtSlot()
    def on_pb_order_list_clicked(self):
        cursor = self.te_editor.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Up)
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine,
        QtGui.QTextCursor.KeepAnchor)
        selection = cursor.selectedText()[:-1]
        last_index = selection.strip()[0]
        if last_index.isdecimal():
            cursor.movePosition(QtGui.QTextCursor.Down)
            listActionHandler.add_start(str(int(last_index) + 1) +". ",cursor)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = kdMarkdownPad()
    win.show()
    sys.exit(app.exec_())
