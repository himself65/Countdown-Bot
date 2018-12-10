from cqhttp import CQHttp
from util import print_log
from register import command, schedule_loop
from global_vars import registered_commands as commands
from global_vars import config
import re
import util
import global_vars


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "倒计时Bot的基本功能."
    }


@command(name="help", help="查看帮助")
def help(bot: CQHttp, context=None, args=None):
    bot.send(context, "".join(
        map(lambda x: x[0]+" --- "+x[1][0]+"\n", commands.items())))


@command(name="status", help="查看Bot运行状态")
def show_status(bot: CQHttp, context, args):
    to_send =\
        """倒计时广播时间: {broadcast_hour:0>2d}:{broadcast_minute:0>2d}
Hitokoto广播时间: {hitokoto_hour:0>2d}:{hitokoto_minute:0>2d}
指令前缀: {command_prefix}
输入 [指令前缀]help 查看帮助""".format(
            broadcast_hour=config.BROADCAST_HOUR, broadcast_minute=config.BROADCAST_MINUTE,
            hitokoto_hour=config.HITOKOTO_HOUR, hitokoto_minute=config.HITOKOTO_MINUTE,
            command_prefix="".join(
                map(lambda x: x+" ", config.COMMAND_PREFIX)),
        )
    bot.send(context, to_send)


@command(name="plugins", help="查看插件列表")
def plugins(bot: CQHttp, context, args):
    def make_msg(obj):
        msg = ""
        for k, v in obj.items():
            msg += "%s = %s\n" % (k, v)
        return msg
    bot.send(context, "".join(
        map(lambda obj: make_msg(obj)+"\n", global_vars.loaded_plugins)))


@command(name="broadcast", help="进行广播")
def broadcast_cmd(bot, context, args=None):
    # print_log("broadcasting..")
    group_id = context.get("group_id", -1)
    if group_id != -1:
        broadcast_at_group(group_id)


@command(name="reload", help="重新加载配置文件")
def reload_config(bot, context, args=None):
    import importlib
    importlib.reload(config)
    for item in dir(config):
        if item.startswith("__"):
            continue
        print("%s = %s" % (item, getattr(config, item)))


@command(name="about", help="关于")
def about(bot: CQHttp, context=None, args=None):
    bot.send(context, "https://gitee.com/yutong_java/Countdown-Bot")
    bot.send(context, "by MikuNotFoundException")


@command(name="阿克", help="阿克")
def ak(bot: CQHttp, context=None, args=None):
    bot.send(context, "您阿克了！")


@command(name="爆零", help="qwq")
def zero(bot: CQHttp, context=None, args=None):
    bot.send(context, "您不会爆零的qwq")


@command(name="凉了", help="凉了?")
def im_cold(bot: CQHttp, context=None, args=None):
    bot.send(context, "qwq您不会凉的~")



def get_countdown_list(url):
    import json
    import urllib
    decoder = json.JSONDecoder()
    result = None
    with urllib.request.urlopen(url) as f:
        result = decoder.decode(f.read().decode("utf-8"))
    return result


def broadcast_at_group(group_id: int, content=None):
    bot = global_vars.VARS["bot"]
    if content is None:
        content = get_countdown_list(config.LIST_URL)
    print_log("Broadcasting at group %d with content %s" % (group_id, content))
    for item in get_broadcast_content(content[str(group_id)]):
        bot.send_group_msg(group_id=group_id, message=item)


@schedule_loop(hour=config.BROADCAST_HOUR, minute=config.BROADCAST_MINUTE, check_interval=config.CHECK_INTERVAL, execute_delay=config.EXECUTE_DELAY, name="Broadcast")
def execute_broadcast():
    text = get_countdown_list(config.LIST_URL)
    for group in text:
        broadcast_at_group(int(group), text)


def get_broadcast_content(broadcast_list: list):
    # print_log("broadcasting..")
    result = []
    countdown_list = broadcast_list
    from datetime import datetime
    from datetime import timedelta
    today = datetime.now()
    for item in countdown_list:
        print_log(item)
        name = item["name"]
        exp_time = datetime.strptime(item["date"], "%Y-%m-%d")
        delta: timedelta = exp_time-today+timedelta(days=1)
        # days=delta.days+1
        mouths = delta.days//30
        days = delta.days % 30
        if delta.days < 0:
            continue
        text = ""
        if delta.days > 0:
            if mouths > 0:
                text = "距离 %s 还有 %d 天 (%d个月%s)." % (
                    name, delta.days, mouths, ("%d天" % days) if days != 0 else "整")
            else:
                text = "距离 %s 还有 %d 天." % (name, delta.days)
        else:
            text = "今天是 %s ." % (name)
        print_log(text)
        result.append(text)
    return result
