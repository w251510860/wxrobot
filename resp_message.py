import time

import static
import requests
import json
import urllib.request


class RespMessage(object):

    @staticmethod
    def turing_robot(text):
        """ 接入图灵机器人 """
        url = static.TURING_ROBOT_URL
        data = {
            'perception': {
                'inputText': {'text': text},
                'selfInfo': {
                    'location': {
                        'city': static.CITY,
                        'province': static.PROVINCE,
                        'street': ''
                    }
                }
            },
            'userInfo': {
                'userId': 'fairy',
                'apiKey': "512770f4c6b74eb2aaf1536354353015",  # 此处修改为自己机器人apikey值
            }
        }
        data = json.dumps(data).encode('utf8')
        http_post = urllib.request.Request(url, data=data, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        ret = json.loads(response.read().decode('utf8'))
        code = ret['results'][0]['resultType']
        values = ret['results'][0].get('values')[code]
        if '限制' in values:
            return '哎，高级聊天功能还在为我亲爱的牛牛开发中...'
        return values

    @staticmethod
    def get_current_system_time():
        """ 获取当前时间 """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 格式化时间，按照 2017-04-15 13:46:32的格式打印出来
        return current_time

    @staticmethod
    def personal_star(cons_name):
        param = {
            'key': static.JUHE_STAR_KEY,
            'consName': cons_name,
            'type': 'today'
        }
        resp = requests.get(url=static.JUHE_URL, params=param, timeout=(10, 20)).json()
        if resp['error_code'] != 0:
            return '抱歉,今天希腊众神放假...'
        return f"星座名称: {resp['name']} \n日期: {resp['datetime']}\n综合指数: {resp['all']}\n幸运色: {resp['color']}\n" \
            f"健康指数: {resp['health']}\n财运指数: {resp['money']}\n幸运数字: {resp['number']}\n" \
            f"今日概述: {resp['summary']}\n工作指数: {resp['work']}"

    @staticmethod
    def weather_searche(city):
        param = {
            'key': static.JUHE_WEATHER_FORECAST,
            'city': city
        }
        resp = requests.get(url=static.JUHE_WEATHER_URL, params=param, timeout=(10, 20)).json()
        print(f'resp -> {resp}')
        if resp['error_code'] != 0:
            return '查什么?有什么好查的...查不出来你敢凶我吗?ㄟ(▔,▔)ㄏ \n什么!你吼我？Σ(oﾟдﾟoﾉ)\n我跟你说，你 完 了，你会失去本宝宝！(σ｀д′)σ'
        result = resp['result']
        return f"下面由本大仙为小猪播报今日{result['city']}天气情况\n今日天气: {result['realtime']['info']}\n" \
            f"气温: {result['realtime']['temperature']}℃\n湿度: {result['realtime']['humidity']}\n" \
            f"风向: {result['realtime']['direct']}\n风力: {result['realtime']['power']}\n" \
            f"空气质量指数: {result['realtime']['aqi']}"

    @staticmethod
    def qingyunke(msg):
        url = f"http://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}"
        resp = requests.get(url, timeout=(10, 20))
        if resp.status_code == 200 and resp.json()['result'] == 0:
            return resp.json()['content']
        return "嗯! 你说的对！(傻子模式)"

    @staticmethod
    def check_id_card_validate(bank_card_num):
        # 校验银行卡号有效性
        url = f'https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?_input_charset' \
            f'=utf-8&cardNo={bank_card_num}%20&cardBinCheck=true'
        ret = requests.get(url)
        if ret.status_code == 200 and ret.json().get('stat', None):
            return ret.json()['validated']
        return '服务已弃用'
