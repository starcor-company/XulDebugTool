#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon, QPicture, QPixmap


class IconTool(object):
    def __init__(self):
        super().__init__()

    def buildQIcon(iconName):
        return QIcon(os.path.join('..', 'resources', 'images', iconName))

    def buildQPixmap(pixmapName):
        return QPixmap(os.path.join('..', 'resources', 'images', pixmapName))
