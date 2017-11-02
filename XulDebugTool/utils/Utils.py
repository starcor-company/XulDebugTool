#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import xmltodict


class Utils(object):
    @staticmethod
    def xml2json(xml, tag):
        # 将xml的某个tag转化成json
        doc = xmltodict.parse(xml)[tag]
        if doc != None:
            str = json.dumps(dict(doc))
            return json.loads(str)
        else:
            return ''
