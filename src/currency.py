#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import sys
import time
import re
import ssl

from workflow import WorkflowLite
import i18n

ssl._create_default_https_context = ssl._create_unverified_context
units = ['', 'cny', 'usd', 'hkd', 'eur', 'jpy', 'krw', 'brl', 'try']

headers = {
  "Referer": "https://finance.sina.com.cn/forex/",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

def currency(type, money = 1):
  forex = (",fx_s%s" % type).join(units)[1:]
  ts = int(round(time.time() * 1000))
  url = 'https://hq.sinajs.cn/?rn=%s&list=%s' % (ts, forex)
  wf.logger.info("request url: %s" % url)
  result = wf.get(url, headers).decode('GB18030', 'ignore')
  pattern = re.compile(r'(\w{3})\="(.*)"')
  currency_list = pattern.findall(result)
  for tuple in currency_list:
    arr = tuple[1].split(',')
    if len(arr) > 9:
      currency_type = tuple[0].upper()

      if type.upper() != currency_type:
        icon = 'icons/%s.png' % currency_type
        cur =  float(arr[8])
        total = cur * money
        rate = round(int(cur) if int(cur) == cur else cur, 4)
        title = "%s -> %s :  %s" % (type.upper(), currency_type, str(total if total == int(total) else round(total, 2)))
        subtitle = i18n.dic['SUCC_SUBTITLE'] + str(rate)
        arg = currency_type
        wf.add_item(title=title, subtitle=subtitle, icon=icon, arg=arg, valid=True)

  wf.send_feedback()

def main(wf):
  args = sys.argv[1:]
  if len(args) > 0:
    command = args[0]
    money = 1
    try:
      if len(args) == 2:
        num = args[1]
        money = float(num)

      currency(command, money)
    except:
      wf.logger.error("error: %s" % sys.exc_info())
      wf.add_item(title=i18n.dic['TITLE_DEFAULT'], subtitle=i18n.dic['SUBTITLE_DEFAULT'], icon='icon.png')
      wf.send_feedback()
  else:
    wf.send_feedback()

if __name__ == '__main__':
  wf = WorkflowLite()
  sys.exit(main(wf))
