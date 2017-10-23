#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon


class IconTool(object):
    def __init__(self):
        super().__init__()

    def buildQIcon(iconName):
        return QIcon(os.path.join('..', 'resources', 'images', iconName))
