# coolq HTTP API的监听地址
API_URL = "http://127.0.0.1:5001/"
# 访问密钥
ACCESS_TOKEN = "sxoiers"
# 密码
SECRET = ""
# 允许的上报地址
POST_ADDRESS = "0.0.0.0"
# 上报端口
POST_PORT = 5002
# 小时和分钟，24时制
BROADCAST_HOUR = 8
BROADCAST_MINUTE = 0
# 一言广播(小时)
HITOKOTO_HOUR = 8
# 分钟
HITOKOTO_MINUTE = 0
# 启用HITOKOTO的群
HITOKOTO_GROUPS = [
    "718459861"
]
# 检查间隔
CHECK_INTERVAL = 5
# 执行延时
EXECUTE_DELAY = 60
# 列表地址
LIST_URL = "https://raw.githubusercontent.com/ZhehaoMi/countdown/master/countdown.json"
OIWIKI_LIST_URL = "https://raw.githubusercontent.com/ZhehaoMi/countdown/master/wikipages.json"
# 一句话被重复几次后会进行复读
REPEAT_TIME_LIMIT = 3
# 指令前缀
COMMAND_PREFIX = ["--", "!!"]
# 执行Python代码的输出长度限制
OUTPUT_LENGTH_LIMIT = 50
# 执行Python代码的时间限制(ms)
EXECUTE_TIME_LIMIT=2000
SAMPLE = {
    "718459861": [
        {
            "name": "Test",
            "date": "2018-11-22"
        },
        {
            "name": "The man who changed China",
            "date": "1926-8-17"
        }
    ]
}
