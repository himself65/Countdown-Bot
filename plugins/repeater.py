from global_vars import repeat_time, last_message, VARS
from cqhttp import CQHttp
from util import print_log
from register import message_listener
from util import print_log
import importlib
import global_vars
config = global_vars.CONFIG[__name__]

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
