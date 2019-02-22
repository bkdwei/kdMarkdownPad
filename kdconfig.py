# coding: utf-8

import os
import json
from fileutil import check_and_create

config_file = os.environ["HOME"] + "/.config/kdMarkdownPad/conf.json"


def init_conf():
    check_and_create(config_file)
    with open(config_file, "r") as f:
        content = f.read()
        if content.strip() != "":
            conf = json.loads(content)
            return conf


def update_conf(cur_file):
    check_and_create(config_file)
    with open(config_file, "w+") as f:
        conf = {}
        conf["cur_file"] = cur_file
        f.write(json.dumps(conf))
        f.flush()
