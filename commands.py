import config
from main import *


@command(name="broadcast", help="进行广播")
def broadcast_cmd(bot, context):
    # print_log("broadcasting..")
    group_id = context.get("group_id", -1)
    if group_id != -1:
        broadcast_at_group(group_id)


@command(name="reload", help="重新加载配置文件")
def reload_config(bot, context):
    import importlib
    importlib.reload(config)
    for item in dir(config):
        if item.startswith("__"):
            continue
        print("%s = %s" % (item, getattr(config, item)))


@command(name="help", help="查看帮助")
def help(bot: CQHttp, context=None):
    bot.send(context, "".join(
        map(lambda x: x[0]+" --- "+x[1][0]+"\n", commands.items())))


@command(name="阿克", help="阿克")
def ak(bot: CQHttp, context=None):
    bot.send(context, "您阿克了！")
