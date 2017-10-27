#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmltodict
import json
pageXml = '''<pages>
<page id="426878758" pageId="page_main_noopsyche" layoutFile="xul_layouts/pages/xul_main_page_noopsyche.xml" behavior="NoopsycheMainPageBehavior" pageClass="MainActivity" taskId="1379" intentFlags="RECEIVER_FOREGROUND" status="stopped" resumeTime="43" readyTime="55" drawing="frames:1147, avg:6.44, min:2.08, max:27.54"/>
<page id="824003288" pageId="page_media_detail" layoutFile="xul_layouts/pages/xul_media_detail_page.xml" behavior="media_detail_behavior" pageClass="CommonActivity" taskId="1379" intentFlags="RECEIVER_FOREGROUND" status="resumed" resumeTime="53" readyTime="61" drawing="frames:2, avg:14.94, min:3.45, max:26.43"/>
</pages>'''

pageXml1 = '''<pages>
<page id="426878758"/>
<page id="824003288" pageId="page_media_detail" />
</pages>'''
# r = dict()
j = xmltodict.parse(pageXml1)['pages']

pages = json.dumps(dict(xmltodict.parse(pageXml1)['pages']))
j = json.loads(pages)
print(type(pages))
print(pages)
print(type(j))
print(j)

print(j['page'])
for page in j['page']:
    print('id ' + page['@id'])

