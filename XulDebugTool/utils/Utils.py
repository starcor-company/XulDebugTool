#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import xmltodict


class Utils(object):
    @staticmethod
    def xml2json(xml, tag):
        # 将xml的某个tag转化成json

        # xml to dict-str
        str = json.dumps(dict(xmltodict.parse(xml)[tag]))
        # str to json
        return json.loads(str)
