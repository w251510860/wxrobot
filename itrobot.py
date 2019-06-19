#!/usr/bin/env python
# coding=utf-8
import itchat
import time
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
    while True:
        current_time = time.localtime(time.time())
        # 定时发送销售
        if current_time.tm_hour % 1 == 0 and current_time.tm_min % 30 == 0:
            replay = u'时间: %s' % (resp_msg.get_current_system_time())
            itchat.send(replay, toUserName="filehelper")
        time.sleep(1000)


def lc():
    print('finish login')
    itchat.send(u'机器人上线 %s' % resp_msg.get_current_system_time(), toUserName='filehelper')  # 发送内容


def ec():
    print('exit')
    itchat.send(u'机器人下线 %s ' % resp_msg.get_current_system_time(), toUserName='filehelper')  # 发送内容


newInstance.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir="newInstance.pkl")

try:
    newInstance.run(debug=True)
except Exception:
    itchat.logout()
