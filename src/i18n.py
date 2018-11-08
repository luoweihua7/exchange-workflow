# -*- coding: utf-8 -*-

import os

_dics = {
  'en_US': {
    'TITLE_DEFAULT' : u'Get Exchange Rate Failure',
    'SUBTITLE_DEFAULT' : u'Please try again...',
    'SUCC_TITLE' : u'Exchanged result：',
    'SUCC_SUBTITLE' : u'Current rate：',
    'ERR_TYPE_TITLE' : u'Please Input Currency',
    'ERR_TYPE_SUBTITLE' : u'eg. USD->CNY, input "usdcny"',
    'ERR_RATE_TITLE' : u'Currency Not Support',
    'ERR_RATE_SUBTITLE' : u'No support for current currency',
  },
  'zh_CN': {
    'TITLE_DEFAULT' : u'汇率转换失败',
    'SUBTITLE_DEFAULT' : u'请重试，或换一个汇率试试...',
    'SUCC_TITLE' : u'转换后金额为：',
    'SUCC_SUBTITLE' : u'当前汇率：',
    'ERR_TYPE_TITLE' : u'请输入需要转换的币种',
    'ERR_TYPE_SUBTITLE' : u'例如：美元兑人民币，输入"usdcny"',
    'ERR_RATE_TITLE' : u'币种不支持',
    'ERR_RATE_SUBTITLE' : u'暂不支持当前币种',
  }
}

local = os.popen('defaults read -g AppleLocale').read().rstrip()

try:
  dic = _dics[local]
except KeyError as e:
  dic = _dics['en_US']


  