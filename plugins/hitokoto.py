from cqhttp import CQHttp
from util import print_log
from register import command, schedule_loop
from global_vars import registered_commands as commands
from global_vars import config as global_config
import global_vars
import re
import util
config = global_vars.CONFIG[__name__]

def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "Hitokoto广播器"
    }





@command(name="hitokoto", help="发送一言")
def hitokoto(bot: CQHttp, context=None, args=None):
    import util
    bot.send(context, get_hitokoto())


def get_hitokoto():
    import urllib3
    import json
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    response = http.urlopen(url="https://v1.hitokoto.cn/", method="GET")
    data = json.JSONDecoder().decode(response.data.decode())
    response.close()
    to_send =\
        """{text}
            
--- {source}
    
(Hitokoto ID:{id})""".format(text=data["hitokoto"], source=data["from"], id=data["id"])
    return to_send


def get_hitokoto_groups(url):
    broadcast_list = url
    if type(broadcast_list) is str:
        import json
        import util
        broadcast_list = json.JSONDecoder().decode(
            util.get_text_from_url(broadcast_list))
    return broadcast_list


@schedule_loop(hour=config.HITOKOTO_HOUR, minute=config.HITOKOTO_MINUTE, check_interval=global_config.CHECK_INTERVAL, execute_delay=global_config.EXECUTE_DELAY, name="Hitotoko")
def execute_hitokoto_broadcast():
    bot = global_vars.VARS["bot"]
    message = get_hitokoto()
    import util
    for group_id in get_hitokoto_groups(config.HITOKOTO_BROADCAST_LIST):
        bot.send_msg(message_type="group", group_id=int(
            group_id), message=message)
