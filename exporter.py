#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import markdown
from pymd2doc import createDoc

def export2html(content,file_path):
    html = markdown.markdown(content)
    with open(file_path,"w+") as f:
        f.write(html)

def export2pdf(content,file_path):


