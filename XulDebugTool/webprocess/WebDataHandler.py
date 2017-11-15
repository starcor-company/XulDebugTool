#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from XulDebugTool.utils.Utils import Utils


class WebDataHandler():
    def readData(self,str):
        dict = json.loads(str)
        action = dict['action']
        if action == "click":
            id = dict['Id']
            xml = dict['xml']
            element = Utils.findNodeById(id, xml)
            print('receive %s' % element.tag)
            print('receive %s' % element.text)
            print('receive %s' % element.attrib)
            #     获得element的子集用getchildren()
            #     children = element.getchildren()
            #     if len(children):
            #         print(element.text + " " + children[0].text)
            #     else:
            #         print(element.text)