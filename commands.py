#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from main import *


@command(name="status", help="查看状态")
def show_status(bot: CQHttp, context, args):
    to_send =\
        """倒计时广播时间: {broadcast_hour:0>2d}:{broadcast_minute:0>2d}
Hitokoto广播时间: {hitokoto_hour:0>2d}:{hitokoto_minute:0>2d}
进行Hitokoto广播的群: {hitokoto_groups}
指令前缀: {command_prefix}
输入 [指令前缀]help 查看帮助""".format(
            broadcast_hour=config.BROADCAST_HOUR, broadcast_minute=config.BROADCAST_MINUTE,
            hitokoto_hour=config.HITOKOTO_HOUR, hitokoto_minute=config.HITOKOTO_MINUTE,
            hitokoto_groups="".join(
                map(lambda x: x+" ", config.HITOKOTO_GROUPS)),
            command_prefix="".join(
                map(lambda x: x+" ", config.COMMAND_PREFIX)),
        )
    bot.send(context, to_send)


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


@command(name="help", help="查看帮助")
def help(bot: CQHttp, context=None, args=None):

    bot.send(context, "".join(
        map(lambda x: x[0]+" --- "+x[1][0]+"\n", commands.items())))


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
def zero(bot: CQHttp, context=None, args=None):
    bot.send(context, "qwq您不会凉的~")


@command(name="oier", help="执行oierdb查询(http://bytew.net/OIer)")
def oier_query(bot: CQHttp, context=None, args=None):
    print_log("querying "+str(args))
    if len(args) < 2:
        bot.send(context, "请输入姓名qwq")
        return
    import threading

    def query():
        from util import print_log
        # print_log("querying "+args[1])
        text = "查询到以下数据:\n"
        # bot.send(context,"查询到以下数据:")
        import oierdb
        from random import shuffle
        count = 0
        items = oierdb.fetch(args[1])
        shuffle(items)
        for item in items:
            print_log("item:{}".format(item))
            text += "姓名:%s\n性别:%s\n" % (item["name"],
                                        {-1: "女", 1: "男"}.get(int(item["sex"]), "未知"))
            # text+="获得奖项:\n"
            awards = list(enumerate(eval(item["awards"])))
            for index, award in awards:
                # print_log(award)
                # print_log(type(award))
                for k, v in award.items():
                    if type(v) == type(str):
                        award[k] = award[k].strip()
                format_str = "在<{province}>{school}<{grade}>时参加<{contest}>以{score}分(全国排名{rank})的成绩获得<{type}>\n"
                text += format_str.format(grade=award["grade"],
                                          province=award["province"],
                                          rank=award["rank"],
                                          score=award["score"],
                                          school=award["school"],
                                          type=award["award_type"],
                                          contest=award["identity"]
                                          )
            count += 1
            if count >= 5:
                text += "\n余下记录太长，请去原网站查看."
                break
            text += '\n'
        while text[-1] == "\n":
            text = text[:-1]
        bot.send(context, text)
    thread: threading.Thread = threading.Thread(target=query)
    # query()
    thread.start()


@command(name="wiki", help="求助 OI Wiki(https://oi-wiki.org/)")
def oiwiki_query(bot: CQHttp, context=None, args=None):
    # from wikipages import wikipages
    import urllib
    import config
    import json
    wikipages = None
    decoder = json.JSONDecoder()
    with urllib.request.urlopen(config.OIWIKI_LIST_URL) as page:
        wikipages = decoder.decode(page.read().decode("utf-8"))
    query_text = args[1]
    if query_text in wikipages:
        bot.send(context, "OI Wiki 列表中有名为「%s」的页面：%s" %
                 (query_text, wikipages[query_text]))
    else:
        bot.send(context, "OI Wiki 列表中无结果，请访问：https://oi-wiki.org/ 查看更多内容")


@command(name="hitokoto", help="发送一言")
def hitokoto(bot: CQHttp, context=None, args=None):
    import util
    bot.send(context, util.get_hitokoto())


@command(name="exec", help="在Docker中执行一行Python3代码")
def exec_python_code(bot: CQHttp, context=None, args=None):
    try:
        from python_runner import run_python_in_docker
    except Exception as ex:
        bot.send(context, "无法启用Python runner: {}".format(ex))

    def callback(msg):
        bot.send(context, msg)
    run_python_in_docker(callback, "".join(map(lambda x: x+" ", args[1:])))
