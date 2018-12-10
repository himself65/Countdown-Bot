#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from cqhttp import CQHttp
from util import print_log
from global_vars import message_listeners, registered_commands, config, loop_threads, loaded_plugins, loop_threads
from flask import request, make_response
from json import JSONEncoder
import threading
import time
import pdb
import flask
import os
import importlib
# import PyV8 
bot = CQHttp(api_root=config.API_URL, access_token=config.ACCESS_TOKEN)
log = bot.logger
web_app = bot._server_app


@web_app.route("/api/credit/get_by_group/<int:group_id>", methods=["POST", "GET"])
def get_credit_by_group(group_id: int):
    from plugins import sign_in
    import os
    if not os.path.exists(os.path.join(config.ATTENDANCE_DATA, "group-{}.json".format(group_id))):
        return JSONEncoder().encode({
            "message": "Group not found.",
            "status": -1
        })
    return JSONEncoder().encode(sign_in.load_data(group_id))


@web_app.route("/api/credit/get_groups", methods=["POST", "GET"])
def get_groups():
    import os
    import re
    result = []
    pattern = re.compile(r"group-([0-9]+)\.json")
    for group in os.listdir(config.ATTENDANCE_DATA):
        result.append(pattern.findall(group)[0])
    return JSONEncoder().encode(result)


def init():
    print_log("Starting countdown-bot.")
    print_log("By MikuNotFoundException.")
    print_log("QQ:814980678")
    def load_python_plugin(plugin):
        this = importlib.import_module("plugins."+plugin[:plugin.index(".py")])
        if "plugin" in dir(this):
            loaded_plugins.append(dict(**this.plugin(), **{
                "load": getattr(this, "load", None),
                "disable": getattr(this, "disable", None),
                "name": this.__name__
            }))
            if hasattr(this, "load"):
                this.load()
            print_log("Loaded plugin: {}".format(loaded_plugins[-1]))
    def load_javascript_plugin(name):
        pass
    # 加载插件
    for plugin in os.listdir("./plugins"):
        if os.path.isfile(os.path.join("./plugins", plugin)) == False:
            continue
        if plugin.startswith("__"):
            continue
        if plugin.endswith(".py"):
            load_python_plugin(plugin)
        elif plugin.endswith(".js"):
            load_javascript_plugin(plugin)

    print_log("Registered commands:\n{}".format("".join(
        map(lambda x: "{} :{}\n".format(x[0], x[1]), registered_commands.items()))))
    print_log("Registered message listeners:\n{}".format(message_listeners))
    print_log("Registered schedule loops:\n{}".format(loop_threads))
    for x in loop_threads:
        x.start()
    # 启动CQ Bot
    print_log("Starting CQHttp...")
    import global_vars
    global_vars.VARS["bot"] = bot
    bot.run(host=config.POST_ADDRESS, port=config.POST_PORT)


@bot.on_message()
def handle_message(context):
    print_log("Handling message:{}".format(context))
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
            print_log("Execute command: {}".format(command))
            if command[0] in registered_commands:
                registered_commands[command[0]][1].__call__(
                    bot, context, command)
            else:
                bot.send(context, "未知指令: %s" % command[0])
        if text is not None:
            print_log("Calling message listeners.")
            for listener in message_listeners:
                listener.__call__(bot, context, text)


@bot.on_request("group", "friend")
def handle_group_invite(context):
    return {"approve": True}


def input_loop():
    pass


if __name__ == "__main__":
    # pdb.set_trace()
    init()
