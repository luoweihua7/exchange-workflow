#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import sys
import time
import re

from workflow import WorkflowLite
import i18n

base_url = 'https://hq.sinajs.cn/?rn=timestamp&list=fx_s'
headers = {
  "Referer": "https://finance.sina.com.cn/forex/",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

def exchange(convert_type, money = 1):
  if len(convert_type) == 6:
    ts = int(round(time.time() * 1000))
    url = 'https://hq.sinajs.cn/?rn=%s&list=fx_s%s' % (ts, convert_type)
    result = wf.get(url, headers).decode('GB18030', 'ignore')
    match = re.search(r'\"(.*)\"', result)
    if match:
      arr = match.group(1).split(',')
      if len(arr) > 9:
        f_rate = float(arr[8])
        rate = f_rate if int(f_rate) == f_rate else round(f_rate, 2)
        total = round(rate * money, 4)
        coin = convert_type[-3:]
        icon = 'icons/%s.png' % coin.upper()
        title = i18n.dic['SUCC_TITLE'] + str(int(total) if int(total) == total else total)
        subtitle = i18n.dic['SUCC_SUBTITLE'] + str(rate)
        arg = convert_type.upper()
        wf.add_item(title=title, subtitle=subtitle, icon=icon, arg=arg, valid=True)
      else:
        wf.add_item(title=i18n.dic['ERR_RATE_TITLE'], subtitle=i18n.dic['ERR_RATE_SUBTITLE'], icon='icon.png')
    else:
      wf.add_item(title=i18n.dic['TITLE_DEFAULT'], subtitle=i18n.dic['SUBTITLE_DEFAULT'], icon='icon.png')
  else:
    wf.add_item(title=i18n.dic['TITLE_TIP'], subtitle=i18n.dic['SUBTITLE_TIP'], icon='icon.png')

  wf.send_feedback()

def main(wf):
  args = sys.argv[1:]
  if len(args) > 0:
    command = args[0]
    money = 1
    if len(args) == 2:
      num = args[1]
      money = float(num)
    exchange(command, money)
  else:
    wf.add_item(title=i18n.dic['TITLE_TIP'], subtitle=i18n.dic['SUBTITLE_TIP'])
    wf.send_feedback()

if __name__ == '__main__':
  wf = WorkflowLite()
  sys.exit(main(wf))