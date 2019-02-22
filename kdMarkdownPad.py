#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import markdown
from PyQt5.QtCore import pyqtSlot, QFile
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QWidget,
    QMainWindow,
    QApplication,
    QFileDialog,
    QTextBrowser,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import kdconfig


class kdMarkdownPad(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kdMarkdownPad.ui", self)

        # ~ 1未保存,2是已保存
        self.state = 2
        # ~ 改变五次自动预览
        self.change_counter = 0
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

    @pyqtSlot()
    def on_te_editor_textChanged(self):
        self.state = 1
        self.change_counter += 1
        if self.change_counter >= 5:
            self.on_action_preview_triggered()
            self.change_counter = 0

    @pyqtSlot()
    def on_action_new_triggered(self):
        if self.state == 1:
            reply = QMessageBox.information(
                self, "文件尚未保存", "是否保存?", QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.on_action_save_triggered()

        self.cur_file = None
        self.te_editor.clear()
        self.state = 2
        self.statusbar.clearMessage()

    @pyqtSlot()
    def on_action_preview_triggered(self):
        html = markdown.markdown(self.te_editor.toPlainText())
        self.tb_viewer.setHtml(html)

    @pyqtSlot()
    def on_action_open_triggered(self):
        self.get_cur_path()
        file_path = QFileDialog.getOpenFileName(
            None, "open file", self.cur_file, "*.md"
        )

        if file_path[0] == "":
            return
        self.cur_file = file_path[0]
        with open(self.cur_file, "r") as f:
            my_txt = f.read()
            self.change_counter = 5
            self.te_editor.setPlainText(my_txt)
            self.state = 2
        kdconfig.update_conf(self.cur_file)

    @pyqtSlot()
    def on_action_save_triggered(self):
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
            self.statusbar.showMessage("保存文件成功," + self.cur_file)
        kdconfig.update_conf(self.cur_file)

    @pyqtSlot()
    def on_action_handbook_triggered(self):
        with open("markdown语法.md", "r") as f:
            html = markdown.markdown(f.read())
            self.handbook.setHtml(html)
            self.handbook.show()

    def get_cur_path(self):
        if self.cur_file is None:
            return os.path.dirname(self.conf["cur_file"])
        else:
            return os.path.dirname(self.cur_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = kdMarkdownPad()
    win.show()
    sys.exit(app.exec_())
