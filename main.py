#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from cqhttp import CQHttp

try:
    import config
except ModuleNotFoundError as ex:
    import config_default as config
from util import print_log, get_countdown_list, get_hitokoto

import threading
import time
bot = CQHttp(api_root=config.API_URL, access_token=config.ACCESS_TOKEN)
log = bot.logger
commands = {

}

message_listeners = [

]


def command(name, help=""):
    def inner(func):
        commands[name] = (help, func)
    return inner


def message_listener():
    def inner(func):
        message_listeners.append(func)
    return inner

def execute_broadcast():
    text = get_countdown_list(config.LIST_URL)
    for group in text:
        broadcast_at_group(int(group), text)

def execute_hitokoto_broadcast():
    message = get_hitokoto()
    for group_id in config.HITOKOTO_GROUPS:
        bot.send_msg(message_type="group", group_id=int(
            group_id), message=message)


def main():
    print_log("Starting countdown-bot.")
    print_log("By MikuNotFoundException.")
    print_log("QQ:814980678")
    # 启动主循环线程

    broadcast_thread = threading.Thread(target=schedule_loop, args=(config.BROADCAST_HOUR, config.BROADCAST_MINUTE,
                                                                    config.CHECK_INTERVAL, config.EXECUTE_DELAY, execute_broadcast, "Countdown broadcast"))
    hitokoto_thread = threading.Thread(target=schedule_loop, args=(config.HITOKOTO_HOUR, config.HITOKOTO_MINUTE,
                                                                   config.CHECK_INTERVAL, config.EXECUTE_DELAY, execute_hitokoto_broadcast, "Hitokoto broadcast"))

    broadcast_thread.start()
    hitokoto_thread.start()
    # 启动CQ Bot
    print_log("Starting CQHttp...")
    bot.run(host=config.POST_ADDRESS, port=config.POST_PORT)


def broadcast_at_group(group_id: int, content=None):
    if content is None:
        content = get_countdown_list(config.LIST_URL)
    print_log("Broadcasting at group %d with content %s" % (group_id, content))
    for item in get_broadcast_content(content[str(group_id)]):
        bot.send_group_msg(group_id=group_id, message=item)


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


@bot.on_message()
def handle_message(context):
    print_log("handling message:{}".format(context))
    if "group_id" in context:
        text: str = None
        import cqhttp
        if type(context["message"]) is str:
            text = context["message"]
        elif context["message"][0]["type"] == "text":
            text: str = context["message"][0]["data"]["text"]

        def check_prefix(command):
            for item in config.COMMAND_PREFIX:
                if command.startswith(item):
                    return item
        prefix = check_prefix(text)
        if text is not None and prefix is not None:
            command = (text[len(prefix):]+" ").split(" ")
            print_log("execute command: {}".format(command))
            if command[0] in commands:
                commands[command[0]][1].__call__(
                    bot, context, command)
            else:
                bot.send(context, "未知指令: %s" % command[0])
        if text is not None:
            for listener in message_listeners:
                listener.__call__(bot, context, text)


@bot.on_request("group", "friend")
def handle_group_invite(context):
    return {"approve": True}


def schedule_loop(hour: int, minute: int, check_interval: int, execute_delay: int, todo, name="Schedule Task"):
    while True:
        while True:
            from datetime import datetime
            curr = datetime.now()
            if curr.hour == hour and curr.minute == minute:
                break
            print_log("Checking '"+name+"'")
            time.sleep(check_interval)
        print_log("Executing '"+name+"'")
        todo()
        time.sleep(execute_delay)


def input_loop():
    pass


from commands import *
from events import *
if __name__ == "__main__":
    main()
