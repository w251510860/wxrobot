import datetime

import itchat
from apscheduler.schedulers.background import BackgroundScheduler

import static
from resp_message import RespMessage

resp_msg = RespMessage()


def run():
    # 程序入口
    scheduler = BackgroundScheduler()
    scheduler.add_job(keep_alive, 'cron', hour='0-1,10-11,16-17,20-21')
    scheduler.start()
    while True:
        keep_alive()
        print(f'循环一圈...')


def keep_alive():
    def check_alive():
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if check_alive():
        # 如果当前心跳停止，重启
        return True
    itchat.auto_login(enableCmdQR=2, hotReload=True, loginCallback=init_wxrobot, exitCallback=exit_wxrobot)
    itchat.run(blockThread=True)
    return True


def init_wxrobot(schedule=True, *args, **kwargs):
    # 初始化微信机器人,更新好友信息、微信组
    itchat.get_friends(update=True)
    itchat.get_chatrooms(update=True)
    # if schedule:
    #     # 开启定时任务
    #     init_schedule(schedule_list)
    send_notice('机器人已启动...')


def exit_wxrobot():
    # 关闭机器人通知
    send_notice('机器人已关闭...')


def send_notice(text=None):
    # 给微信消息助手发送消息
    if text:
        itchat.send(text, toUserName=static.MSG_NOTICE_ROBOT)


def init_schedule(task_dict_list: list):
    # 初始化定时任务
    if not task_dict_list:
        return
    scheduler = BackgroundScheduler()
    for task_dict in task_dict_list:
        cron_time = task_dict['cron_time']
        task = task_dict['task']
        to_name = task_dict['to_name']
        print(f'task -> {task}, task type -> {type(task)}')
        scheduler.add_job(task, 'cron', **cron_time, args=[to_name])

    scheduler.start()
    print('定时任务已经开启...')


@itchat.msg_register('Text')
def text_reply(msg):
    # 通用文本类聊天接口
    text = msg.text.strip().lower()
    nick_name = msg['User'].NickName
    from_user = msg.get('FromUserName')
    print(f'nick_name -> {nick_name} from_user -> {from_user} text -> {text} text type -> {type(text)}')
    fun = fun_dict.get(text)
    if fun:
        return fun
    if nick_name == 'fairy' and ',' in text:
        name, content = text.split(',')
        itchat.send(f'{content}', toUserName=get_uid(name))
        return '转发成功...'
    if text == '2':
        return '请输入您的城市(不需要加上省、市),如:北京 天气'
    if text == '3':
        return '请输入您的星座,如: 狮子座'
    if text == '4':
        return '请发送以留言+内容,如: 留言,我爱你'
    if text == '5':
        if from_user and from_user in chat_list:
            return '机器人已经开启,请不要重复开启。'
        if from_user:
            chat_list.append(from_user)
            return '聊天机器人开启，如需关闭请发送:close robot'
        return '机器人正在维护中...'
    if text == 'clone robot':
        if from_user:
            chat_list.remove(from_user)
    if from_user in chat_list:
        return resp_msg.qingyunke(text)
    if text.split(' ')[0].endswith('座'):
        return resp_msg.personal_star(text.split(' ')[0])
    if len(text.split(' ')) == 2 and '天气' in text.split(' ')[1]:
        return resp_msg.weather_searche(text.split(' ')[0])
    if text.startswith('留言'):
        itchat.send(f'{nick_name}\n{text}', toUserName=get_uid('fairy'))
        return '留言转发成功...'
    return u"九酱为您服务,请根据下列编号选择服务:\n【1】获取本人手机号\n【2】查天气\n【3】查星座\n" \
           u"【4】留言(将会自动转发至本人)\n【5】聊天(请准备好《莫生气》一本以备不时之需)\n"


def say_hello_every_day(name):
    # 每日问候
    current_time = datetime.datetime.now().hour
    current_day = datetime.datetime.now().weekday()
    if current_time == 7 and current_day <= 5:
        send_msg(name, f'主人,现在已经7点半啦了，赶紧起床！！！ \n再不起床，小酱就要叫爸爸过来掀被子打你PP啦！！！')
        send_msg(name, resp_msg.personal_star('狮子座'))
    if current_time == 11:
        send_msg(name, f'主人,吃完午饭记得要按时午休哦,活力满满的一下午，fighting！！！')
    if current_time == 18:
        send_msg(name, f'主人,准备吃饭咯')
    if current_time == 21:
        send_msg(name, f'主人,现在已经晚上9点多啦了,准备洗漱一下吧！！！ \n\n\n\t\t\t么么哒💕')
    if current_time == 22:
        send_msg(name, f'主人,现在已经夜里10点多了哦,是时候闭上眼美美睡一觉啦！！！ \n\n\n\t\t\t晚安，么么哒💕')


def send_msg(name, msg):
    # 发送消息
    if isinstance(name, str):
        uid = get_uid(name)
        itchat.send(msg, toUserName=uid)
    if isinstance(name, list):
        uid_list = get_uid(name)
        for uid in uid_list:
            itchat.send(msg, toUserName=uid)


def get_uid(name):
    # 获取用户真实id
    if isinstance(name, str):
        return itchat.search_friends(name=name)[0].get('UserName')

    if isinstance(name, list):
        return [itchat.search_friends(name=user_name)[0].get('UserName') for user_name in name]


# 定时任务列表
schedule_list = [{
    'cron_time': {'hour': '7', 'minute': '30'},
    'task': say_hello_every_day,
    'to_name': ['fairy']
}, {
    'cron_time': {'hour': '11', 'minute': '30'},
    'task': say_hello_every_day,
    'to_name': ['fairy']
}, {
    'cron_time': {'hour': '18', 'minute': '30'},
    'task': say_hello_every_day,
    'to_name': ['fairy']
},{
    'cron_time': {'hour': '22', 'minute': '0'},
    'task': say_hello_every_day,
    'to_name': ['fairy']
}, {
    'cron_time': {'hour': '21', 'minute': '0'},
    'task': say_hello_every_day,
    'to_name': ['fairy']
}]

# 功能列表
fun_dict = {
    '1': resp_msg.phone_num(),
}

# 聊天列表
chat_list = []