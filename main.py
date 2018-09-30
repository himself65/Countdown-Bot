from util import print_log, get_countdown_list
from cqhttp import CQHttp
import config
import threading
import time
bot = CQHttp(api_root=config.API_URL, access_token=config.ACCESS_TOKEN)
log = bot.logger
commands = {

}


def command(name, help=""):
    def inner(func):
        commands[name] = (help, func)
    return inner


def main_loop():
    while True:
        while True:
            from datetime import datetime
            curr = datetime.now()
            if curr.hour == config.BROADCAST_HOUR and curr.minute == config.BROADCAST_MINUTE:
                break
            print_log("checking... ")
            time.sleep(config.CHECK_INTERVAL)
        print_log("broadcast at time table.")
        text = get_broadcast_content()
        for group in config.GROUP_ID:
            bot.send_group_msg(group_id=group, message=text)
        time.sleep(config.EXECUTE_DELAY)


def input_loop():
    while True:
        command = input()


def main():
    print_log("Starting countdown-bot.")
    print_log("By MikuNotFoundException.")
    print_log("QQ:814980678")
    print_log("Starting CQHttp...")
    thread = threading.Thread(target=main_loop)
    print_log("Starting daemon thread..")
    thread.start()
    input_thread = threading.Thread(target=input_loop)
    print_log("Starting input thread..")
    input_thread.start()
    bot.run(host=config.POST_ADDRESS, port=config.POST_PORT)


@command(name="broadcast", help="进行广播")
def broadcast_cmd(bot: CQHttp=bot, context=None):
    print_log("broadcasting..")
    for item in get_broadcast_content():
        bot.send(context, item)


@command(name="reload", help="重新加载配置文件")
def reload_config(bot, context):
    import importlib
    importlib.reload(config)
    for item in dir(config):
        if item.startswith("__"):
            continue
        print("%s = %s" % (item, getattr(config, item)))


def get_broadcast_content():
    # print_log("broadcasting..")
    result = []
    countdown_list = get_countdown_list()
    from datetime import datetime
    from datetime import timedelta
    today = datetime.now()
    for item in countdown_list:
        print_log(item)
        name = item["name"]
        exp_time = datetime.strptime(item["date"], "%Y-%m-%d")
        delta: timedelta = exp_time-today
        mouths = delta.days//30
        days = delta.days % 30
        if delta.days < 0:
            continue
        text = "距离 %s 还有 %d 天 (%d个月%s)." % (
            name, delta.days, mouths, ("%d天" % days) if days != 0 else "整")
        print_log(text)
        result.append(text)


@command(name="help", help="查看帮助")
def help(bot: CQHttp, context=None):
    bot.send(context, "".join(
        map(lambda x: x[0]+" --- "+x[1][0]+"\n", commands.items())))


@bot.on_message()
def handle_message(context):
    print_log("handling message:{}".format(context))
    # print_log(context)
    if context.get("group_id", -1) in config.GROUP_ID
        text: str = None
        # print_log(context["message"])
        # print_log(type(context["message"]))
        import cqhttp
        if type(context["message"]) is str:
            text = context["message"]
        elif context["message"][0]["type"] == "text":
            text: str = context["message"][0]["data"]["text"]
        if text is not None and text.startswith("/"):
            command = text[1:]
            if command in commands:
                commands[command][1].__call__(bot, context)


if __name__ == "__main__":
    main()
