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


class kdMarkdownPad(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kdMarkdownPad.ui", self)
        self.change_counter = 0
        # ~ 0是新建状态,1未保存,2是已保存
        self.state = 0
        self.handbook = QWebEngineView()

        html = markdown.markdown(self.te_editor.toPlainText())
        self.tb_viewer.setHtml(html)
        self.te_editor.clear()

    @pyqtSlot()
    def on_te_editor_textChanged(self):
        self.state = 1
        self.change_counter += 1
        if self.change_counter >= 5:
            self.on_action_preview_triggered()
            self.chain_couter = 0

    @pyqtSlot()
    def on_action_new_triggered(self):
        print("新建")
        self.state = 0

    @pyqtSlot()
    def on_action_preview_triggered(self):
        html = markdown.markdown(self.te_editor.toPlainText())
        self.tb_viewer.setHtml(html)

    @pyqtSlot()
    def on_action_open_triggered(self):
        print("open")
        self.file_path = QFileDialog.getOpenFileName(
            None, "open file", os.environ["HOME"], "*.md"
        )
        print(self.file_path)
        if self.file_path[0] == "":
            return
        with open(self.file_path[0], "r") as f:
            my_txt = f.read()
            self.te_editor.setPlainText(my_txt)
            self.state = 2

    @pyqtSlot()
    def on_action_save_triggered(self):
        self.file_path = QFileDialog.getSaveFileName(
            self, "save file", os.environ["HOME"]
        )
        if self.file_path[0] == "":
            return
        with open(self.file_path[0], "w") as f:
            f.write(self.te_editor.toPlainText())
            print("保存文件成功")
            self.state = 2

    @pyqtSlot()
    def on_action_handbook_triggered(self):
        with open("markdown语法.md", "r") as f:
            html = markdown.markdown(f.read())
            self.handbook.setHtml(html)
            self.handbook.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = kdMarkdownPad()
    win.show()
    sys.exit(app.exec_())
