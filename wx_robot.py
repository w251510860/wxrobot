import datetime

import itchat
from apscheduler.schedulers.background import BackgroundScheduler

import static
from resp_message import RespMessage

resp_msg = RespMessage()

my_chat = itchat


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
            if my_chat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if check_alive():
        # 如果当前心跳停止，重启
        return True
    my_chat.auto_login(enableCmdQR=2, hotReload=True, loginCallback=init_wxrobot, exitCallback=exit_wxrobot)
    my_chat.run(blockThread=True)
    return True


def init_wxrobot(schedule=True, *args, **kwargs):
    # 初始化微信机器人,更新好友信息、微信组
    my_chat.get_friends(update=True)
    my_chat.get_chatrooms(update=True)
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
        my_chat.send(text, toUserName=static.MSG_NOTICE_ROBOT)


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


@my_chat.msg_register('Text')
def text_reply(msg):
    # 通用文本类聊天接口
    text = msg.text.strip().lower()
    nick_name = msg['User'].NickName
    from_user = msg.get('FromUserName')
    if nick_name in ['佩奇牛']:
        public_chat(text, nick_name, from_user)
    if nick_name in ['你怎么可以这么帅?']:
        private_chat(text)
    print(f'nick_name -> {nick_name} from_user -> {from_user} text -> {text} text type -> {type(text)}')


def private_chat(text):
    # 私人定制方法
    pass


def statistics_friend():
    # 统计好友数据
    friend_list = my_chat.get_friends(update=True)[0:]
    # 排除掉自己和微信助手
    total_friend_list = friend_list[1:]
    # 好友总数
    total_friend_no = len(total_friend_list)
    # 统计性别
    sex_map = {
        1: 'male',
        2: 'female'
    }
    sex_list = [sex_map.get(friend['Sex'], 'unknown') for friend in total_friend_list]
    sex_count = {
        'male': sex_list.count('male'),
        'female': sex_list.count('female'),
        'unknown': sex_list.count('unknown'),
    }
    sex_distribution_ratio = {
        'male': f"{round(sex_list.count('male') / total_friend_no * 100, 2)}%",
        'female': f"{round(sex_list.count('female') / total_friend_no * 100, 2)}%",
        'unknown': f"{round(sex_list.count('unknown') / total_friend_no * 100, 2)}%",
    }
    print(f'sex_count -> {sex_count}')
    print(f'sex_distribution_ratio -> {sex_distribution_ratio}')
    # 统计地区
    total_province_list = list(set(friend['Province'] if friend['Province'] else '未知省份' for friend in total_friend_list))
    total_province_dict = {province: 0 for province in total_province_list}
    total_city_list = list(set(friend['City'] if friend['City'] else '未知城市' for friend in total_friend_list))
    total_city_dict = {city: 0 for city in total_city_list}
    print(f'您的好友来自{len(total_province_list)}个省份的{len(total_city_list)}个城市')
    for friend in total_friend_list:
        friend['Province'] = friend['Province'] if friend['Province'] else '未知省份'
        friend['City'] = friend['City'] if friend['City'] else '未知城市'
        total_province_dict[friend['Province']] += 1
        total_city_dict[friend['City']] += 1
    province_ratio = {province: f'{round(province_person_num / total_friend_no * 100, 2)}%'
                      for province, province_person_num in total_province_dict.items()}
    city_ratio = {city: f'{round(city_person_num / total_friend_no * 100, 2)}%'
                  for city, city_person_num in total_city_dict.items()}
    print(f'province_ratio -> {province_ratio}')
    print(f'city_ratio -> {city_ratio}')


def public_chat(text, nick_name, from_user):
    # 公共聊天方法
    fun = fun_dict.get(text)
    if fun:
        return fun
    if nick_name == 'fairy' and ',' in text:
        name, content = text.split(',')
        my_chat.send(f'{content}', toUserName=get_uid(name))
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
    if text == 'close robot':
        if from_user and from_user in chat_list:
            chat_list.remove(from_user)
            return '机器人已关闭'
    if from_user in chat_list:
        return resp_msg.qingyunke(text)
    if text.split(' ')[0].endswith('座'):
        return resp_msg.personal_star(text.split(' ')[0])
    if len(text.split(' ')) == 2 and '天气' in text.split(' ')[1]:
        return resp_msg.weather_searche(text.split(' ')[0])
    if text.startswith('留言'):
        my_chat.send(f'{nick_name}\n{text}', toUserName=get_uid('fairy'))
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
        my_chat.send(msg, toUserName=uid)
    if isinstance(name, list):
        uid_list = get_uid(name)
        for uid in uid_list:
            my_chat.send(msg, toUserName=uid)


def get_uid(name):
    # 获取用户真实id
    if isinstance(name, str):
        return my_chat.search_friends(name=name)[0].get('UserName')

    if isinstance(name, list):
        return [my_chat.search_friends(name=user_name)[0].get('UserName') for user_name in name]


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
}, {
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
