#!/usr/bin/env python
# coding=utf-8
import datetime

import itchat
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from interval import Interval
from resp_message import RespMessage
import static

newInstance = itchat.new_instance()
resp_msg = RespMessage()


def is_work_time():
    """ 判读是否是工作时间  23:00-6:00 """
    current_hour = time.strftime('%H', time.localtime())
    hour = int(current_hour)
    if hour in Interval(0, 7):
        return True
    return False


@newInstance.msg_register('Text')
def text_reply(msg):
    text = msg.text.strip()
    if text.lower() == "help":
        return u"[老爸在修仙，现在我是山大王ψ(｀∇´)ψ]\n输入信息 我们就可以愉快的聊天啦~\n 获取联系方式请回复phone" \
               u" \n例如:北京天气\n讲个笑话\n故事来一个\n......".format(static.NICKNAME)
    elif text.startswith("phone"):
        return u"看在你这么会说话的份上就告诉你吧o(*￣3￣)o\n{}的手机号是:{}\n\n一般人我不告诉他~\n".format(
            static.NICKNAME, static.PHONE_NUMBER)
    elif text.split(' ')[0].endswith('座'):
        return resp_msg.personal_star(text.split(' ')[0])
    elif len(text.split(' ')) == 2 and '天气' in text.split(' ')[1]:
        return resp_msg.weather_searche(text.split(' ')[0])
    else:
        return resp_msg.qingyunke(msg['Text'])
        # input_msg = msg['Text']
        # response_msg = resp_msg.turing_robot(input_msg)
        # return u"{}".format(response_msg)


def send_task():
    """ 发送定时任务 """
    name_list = [('fairy', '北京'), ('Sherry🌵', '上海')]
    for name, city in name_list:
        try:
            itcaht_user_name = newInstance.search_friends(name=name)[0]['UserName']
            current_time = datetime.datetime.now().hour
            if current_time == 7:
                newInstance.send(f'主人,现在已经7点半啦了，赶紧起床！！！ \n再不起床，小酱就要叫爸爸过来掀被子打你PP啦！！！',
                                 toUserName=itcaht_user_name)
                newInstance.send_msg(resp_msg.weather_searche(city), toUserName=itcaht_user_name)
            if current_time == 11:
                newInstance.send(f'主人,吃完午饭记得要按时午休哦，活力满满的一下午，fighting！！！', toUserName=itcaht_user_name)
            if current_time == 22:
                newInstance.send(f'主人,现在已经10点多啦了，是时候闭上眼美美睡一觉啦！！！ \n\n\n\t\t\t晚安，么么哒💕',
                                 toUserName=itcaht_user_name)
        except Exception as e:
            print(f'error -> {e}')


def lc():
    print('finish login')
    itchat.send(u'机器人上线 %s' % resp_msg.get_current_system_time(), toUserName='filehelper')  # 发送内容


def ec():
    print('exit')
    itchat.send(u'机器人下线 %s ' % resp_msg.get_current_system_time(), toUserName='filehelper')  # 发送内容


scheduler = BlockingScheduler()
scheduler.add_job(send_task, 'cron', day_of_week='0-5', hour=7, minute=10)
scheduler.add_job(send_task, 'cron', day_of_week='0-5', hour=11, minute=40)
scheduler.add_job(send_task, 'cron', day_of_week='0-5', hour=22, minute=44)
scheduler.start()

newInstance.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir="newInstance.pkl")

try:
    newInstance.run(debug=True)
except Exception:
    itchat.logout()
