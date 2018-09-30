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


def main():
    print_log("Starting countdown-bot.")
    print_log("By MikuNotFoundException.")
    print_log("QQ:814980678")
    # 启动主循环线程
    loop_thread = threading.Thread(target=main_loop)
    print_log("Starting daemon thread..")
    loop_thread.start()
    # 启动输入线程
    input_thread = threading.Thread(target=input_loop)
    print_log("Starting input thread..")
    input_thread.start()
    # 启动CQ Bot
    print_log("Starting CQHttp...")
    bot.run(host=config.POST_ADDRESS, port=config.POST_PORT)


def broadcast_at_group(group_id: int, content=None):
    if content is None:
        content = get_countdown_list()
    print_log("broadcasting at group %d with content %s" % (group_id, content))
    for item in get_broadcast_content(content[str(group_id)]):
        bot.send_group_msg(group_id=group_id, message=item)


def get_broadcast_content(broadcast_list):
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
        delta: timedelta = exp_time-today
        mouths = delta.days//30
        days = delta.days % 30
        if delta.days < 0:
            continue
        text = "距离 %s 还有 %d 天 (%d个月%s)." % (
            name, delta.days, mouths, ("%d天" % days) if days != 0 else "整")
        print_log(text)
        result.append(text)
    return result


@bot.on_message()
def handle_message(context):
    print_log("handling message:{}".format(context))
    # print_log(context)
    if "group_id" in context:
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
            print_log("execute command:"+command)
            if command in commands:
                commands[command][1].__call__(bot, context)


@bot.on_request("group", "friend")
def handle_group_invite(context):
    return {"approve": True}


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
        text = get_countdown_list()
        for group in text:
            broadcast_at_group(int(group), text)
        time.sleep(config.EXECUTE_DELAY)


def input_loop():
    # while True:
    #     command = input()


from commands import *

if __name__ == "__main__":
    main()
