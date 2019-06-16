# 图灵机器人配置
# API URL
TURING_ROBOT_URL = "http://openapi.tuling123.com/openapi/api/v2"
# API KEY
APIKEY_LIST = [
    '512770f4c6b74eb2aaf1536354353015',
]
# 响应状态码
RESP_CODE = {
    5000: '无解析结果',
    6000: '暂不支持该功能',
    4000: '请求参数格式错误',
    4001: '加密方式错误',
    4002: '无功能权限',
    4003: '该apikey没有可用请求次数',
    4005: '无功能权限',
    4007: 'apikey不合法',
    4100: 'userid获取失败',
    4200: '上传格式错误',
    4300: '批量操作超过限制',
    4400: '没有上传合法userid',
    4500: 'userid申请个数超过限制',
    4600: '输入内容为空',
    4602: '输入文本内容超长(上限150)',
    7002: '上传信息失败',
    8008: '服务器错误',
    0: '上传成功',
}

# 地址
CITY = '北京'
PROVINCE = '北京'

# 昵称 手机号
NICKNAME = u"清蒸九酱"  # 此处修改为您的昵称
PHONE_NUMBER = u"17630700065"  # 此处修改为您的联系方式

# 聚合数据
JUHE_URL = 'http://web.juhe.cn:8080/constellation/getAll'
JUHE_WEATHER_URL = 'http://apis.juhe.cn/simpleWeather/query'
JUHE_STAR_KEY = '39c0317d4d2a86876d861c4183835c22'
JUHE_ZHOUGONG_KEY = 'f9266d68c58a81ccb584002fc60bd269'
JUHE_WEATHER_FORECAST = '1fc0cf7386eaec034d41ae0355a3bf76'
JUHE_NEWS_TOP = 'e7c3c0f490b7f64350edfe5791294ff3'
