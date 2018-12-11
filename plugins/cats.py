from register import command
from cqhttp import CQHttp
from util import print_log
import global_vars
import re
import oss2
import requests
import json
import threading
import random
import tempfile
import shutil
import base64
try:
    import plugins.config.cats_config as config
except ImportError as ex:
    import plugins.config.cats_config_default as config


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "吸猫插件"
    }


def load():
    auth = oss2.Auth(config.ACCESS_KEY_ID, config.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, config.ENDPOINT, config.BUCKET_NAME)
    global_vars.VARS["bucket"] = bucket


@command(name="吸猫", help="吸猫")
def suck_cats(bot: CQHttp, context, args):
    data = load_data()
    bucket: oss2.Bucket = global_vars.VARS["bucket"]
    if len(data) == 0:
        bot.send(context, "目前无人上传过猫猫图片.")
        return
    selected_user = None
    while args[-1] == "":
        del args[-1]
    if len(args) < 2:
        selected_user = random.choice(list(data.keys()))
    else:
        selected_user = args[1]
    print_log("user:{}".format(selected_user))
    if selected_user not in data:
        bot.send(context, "指定用户未上传过猫片")
        return
    selected_index = random.randint(1, data[selected_user]["count"])

    def send():
        file_name = "{}/{}.jpg".format(selected_user, selected_index)
        try:
            stream = bucket.get_object(
                file_name)
            encode = base64.encodebytes(
                stream.read()).decode().replace("\n", "")
            # print_log(encode)
            bot.send(context, "[CQ:image,file=base64://{}]\n来自{}的猫片{}.jpg".format(
                encode, selected_user, selected_index))
        except Exception as ex:
            pass
    threading.Thread(target=send).start()


@command(name="upload", help="上传猫猫图片")
def upload_cats(bot: CQHttp, context, args):
    if len(args) < 2:
        bot.send(context, "请上传图片!")
        return
    uploader_id = str(context["sender"]["user_id"])

    def allocate_file_name():
        data = load_data()
        if uploader_id not in data:
            data[uploader_id] = {"count": 0}
        data[uploader_id]["count"] += 1
        save_data(data)
        return "{}/{}.jpg".format(uploader_id, data[uploader_id]["count"])
    pattern = re.compile(r"\[CQ:image.+url\=(?P<url>[^\[^\]]+)\]")
    result = pattern.search(args[1])
    if result is None:
        bot.send(context, "请上传图片")
        return
    url = result.group("url")
    bucket = global_vars.VARS["bucket"]

    def upload_image():
        name = allocate_file_name()
        print_log("Uploading %s" % name)
        bot.send(context, "{} 的猫猫图片 {} 开始上传.".format(uploader_id, name))
        bucket.put_object(name, requests.get(url))
        bot.send(context, "{} 的猫猫图片 {} 上传完成.".format(uploader_id, name))
    threading.Thread(target=upload_image).start()


def load_data()->dict:
    print_log(__file__)
    import os
    print_log(os.sys.path)
    config_path = os.path.join(os.sys.path[0], "plugins/data/cats.json")
    if not os.path.exists(config_path):
        with open(config_path, "w") as file:
            file.write("{}")
    with open(config_path, "r") as file:
        text = file.read()
        obj = json.JSONDecoder().decode(text)
    return obj


def save_data(obj: dict):
    with open("plugins/data/cats.json", "w") as file:
        json.dump(obj, file)
