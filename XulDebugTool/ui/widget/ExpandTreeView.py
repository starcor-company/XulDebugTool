#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeView


class ExpandTreeView(QTreeView):
    def __init__(self, model):
        super(ExpandTreeView, self).__init__()
        self.setModel(model)
        self.expanded.connect(self.expand)
        self.collapsed.connect(self.collapse)

    def expand(self, index):
        self.model().getItem(index).quicklink_expanded = True

    def collapse(self, index):
        self.model().getItem(index).quicklink_expanded = False
