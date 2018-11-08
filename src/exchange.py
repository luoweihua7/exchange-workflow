#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import json
import urllib
import urllib2
import sys
import time
import re

from workflow import Workflow3
import i18n

reload(sys)
sys.setdefaultencoding('utf-8')

base_url = 'https://hq.sinajs.cn/?rn=timestamp&list=fx_s'

def exchange(convert_type, money = 1):
	if len(convert_type) == 6:
		ts = int(round(time.time() * 1000))
		url = 'https://hq.sinajs.cn/?rn=%s&list=fx_s%s' % (ts, convert_type)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		result = response.read()
		match = re.search(r'\"(.*)\"', result)
		if match:
			arr = match.group(1).split(',')
			rate = float(arr[8])

			coin = convert_type[-3:]
			icon = 'icons/%s.png' % coin.upper()
			title = i18n.dic['SUCC_TITLE'] + str(rate * money)
			subtitle = i18n.dic['SUCC_SUBTITLE'] + str(rate)
			arg = convert_type.upper()
			wf.add_item(title=title, subtitle=subtitle, icon=icon, arg=arg, valid=True)
		else:
			wf.add_item(title=i18n.dic['TITLE_DEFAULT'], subtitle=i18n.dic['SUBTITLE_DEFAULT'], icon='icon.png')
	else:
		wf.add_item(title=i18n.dic['ERR_TYPE_TITLE'], subtitle=i18n.dic['ERR_TYPE_SUBTITLE'], icon='icon.png')

	wf.send_feedback()

def main(wf):
	if len(wf.args) > 0:
		command = wf.args[0]
		money = 1
		if len(wf.args) == 2:
			num = wf.args[1]
			money = float(num)
		exchange(command, money)

if __name__ == '__main__':
	wf = Workflow3()
	sys.exit(wf.run(main))