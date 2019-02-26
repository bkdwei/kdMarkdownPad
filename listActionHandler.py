#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import QWidget,QAction
from PyQt5 import Qt
from PyQt5 import QtGui

bold = [QAction("**"),QAction("__")]
headdings = [QAction("标题1"),QAction("标题2")]
unsort_lists = [QAction("*"),QAction("+"),QAction("-")]


def handle_action(action,cursor):
    text = action.text()
    if action in headdings:
        handle_heading(text,cursor)
    elif action in unsort_lists:
        handle_unsort_list(text,cursor)
    elif action in bold:
        handle_bold(text,cursor)

def handle_heading(text,cursor):
    t = '#'*int(text[2]) +' '
    add_start(t,cursor)
def handle_unsort_list(text,cursor):
    # ~ add_before_and_after(cursor,text + ' ', ' ' + text)
    t = text + ' '
    add_start(t,cursor)
def handle_bold(text,cursor):
    add_before_and_after(' ' + cursor,text + ' ', ' ' + text + ' ')


def add_start(text,cursor):
    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
    cursor.insertText(text)

def add_before_and_after(cursor,text_before,text_after):
    print(cursor.anchor(),cursor.position())
    anchor = cursor.anchor()
    position = cursor.position()
    selected_text_length = len(cursor.selectedText())
    cursor.clearSelection()
    cursor.setPosition(anchor)
    cursor.insertText(text_before)
    cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor,selected_text_length)
    # ~ cursor.setPosition(position + selected_text_length + 3)
    cursor.insertText(text_after)
