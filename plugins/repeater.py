from global_vars import config, repeat_time, last_message
from cqhttp import CQHttp
from util import print_log
from register import message_listener


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "复读机."
    }


@message_listener
def repeat_handler(bot: CQHttp, context, message):
    global last_message, repeat_time
    if message == last_message:
        repeat_time += 1
    else:
        last_message = message
        repeat_time = 1
    if repeat_time >= config.REPEAT_TIME_LIMIT:
        bot.send(context, message)
        repeat_time = 0
        last_message = None
