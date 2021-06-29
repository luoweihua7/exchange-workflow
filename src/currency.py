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

units = ['', 'cny', 'usd', 'hkd', 'eur', 'jpy']

def currency(type, money = 1):
  forex = (",fx_s%s" % type).join(units)[1:]
  ts = int(round(time.time() * 1000))
  url = 'https://hq.sinajs.cn/?rn=%s&list=%s' % (ts, forex)
  wf.logger.info("request url: %s" % url)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  result = response.read()

  pattern = re.compile(r'(\w{3})\="(.*)"')
  currency_list = pattern.findall(result)
  for tuple in currency_list:
    arr = tuple[1].split(',')
    wf.logger.info("translate word: %s ==> %s, %s" % (tuple[0].upper(), len(arr), tuple))
    if len(arr) > 9:
      currency_type = tuple[0].upper()
      icon = 'icons/%s.png' % currency_type
      cur =  float(arr[8]) * money
      rate = int(cur) if int(cur) == cur else cur
      title = "%s -> %s :  %s" % (type.upper(), currency_type, str(rate))
      subtitle = i18n.dic['SUCC_SUBTITLE'] + str(rate)
      arg = currency_type
      wf.add_item(title=title, subtitle=subtitle, icon=icon, arg=arg, valid=True)

  wf.send_feedback()

def main(wf):
  if len(wf.args) > 0:
    command = wf.args[0]
    money = 1
    try:
      if len(wf.args) == 2:
        num = wf.args[1]
        money = float(num)

      currency(command, money)
    except:
      wf.add_item(title=i18n.dic['TITLE_DEFAULT'], subtitle=i18n.dic['SUBTITLE_DEFAULT'], icon='icon.png')
      wf.send_feedback()
  else:
    wf.send_feedback()

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
