from util import print_log, get_countdown_list
from cqhttp import CQHttp
from config import *
import threading
import time
bot = CQHttp(api_root=API_URL, access_token=ACCESS_TOKEN)
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
            if curr.hour == BROADCAST_HOUR and curr.minute == BROADCAST_MINUTE:
                break
            print_log("checking... ")
            time.sleep(20)

        broadcast(bot)


def main():
    print_log("Starting countdown-bot.")
    print_log("By MikuNotFoundException.")
    print_log("QQ:814980678")
    print_log("Starting CQHttp...")
    thread = threading.Thread(target=main_loop)
    print_log("Starting daemon thread..")
    thread.start()
    bot.run(host=POST_ADDRESS, port=POST_PORT)


@command(name="broadcast", help="进行广播")
def broadcast(bot: CQHttp, context=None):
    print_log("broadcasting..")
    countdown_list = get_countdown_list()
    from datetime import datetime
    today = datetime.now()
    for item in countdown_list:
        print_log(item)
        name = item["name"]
        exp_time = datetime.strptime(item["date"], "%Y-%m-%d")
        delta = exp_time-today
        text = "距离 %s 还有 %d 天." % (name, delta.days)
        print_log(text)
        bot.send_group_msg(group_id=GROUP_ID, message=text)


@command(name="help", help="查看帮助")
def help(bot: CQHttp, context=None):
    bot.send(context, "".join(
        map(lambda x: x[0]+" --- "+x[1][1]+"\n", commands.items())))


@bot.on_message()
def handle_message(context):
    print_log("handling message:{}".format(context))
    print_log(context)
    text: str = context["message"]
    if text.startswith("/"):
        command = text[1:]
        if command in commands:
            commands[command][1].__call__(bot, context)


if __name__ == "__main__":
    main()
