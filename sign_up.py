#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


def load_data(group_id):
    from global_vars import config
    import os
    import json
    file_path = os.path.join(config.ATTENDANCE_DATA,
                             "group-%s.json" % (group_id))
    # 文件不存在，建立文件夹
    if not os.path.exists(config.ATTENDANCE_DATA):
        os.makedirs(config.ATTENDANCE_DATA)

    # 读取json文件
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    return data


def save_data(data, group_id):
    from global_vars import config
    import os
    import json
    file_path = os.path.join(config.ATTENDANCE_DATA,
                             "group-%s.json" % (group_id))
    # 文件不存在，建立文件夹
    if not os.path.exists(config.ATTENDANCE_DATA):
        os.makedirs(config.ATTENDANCE_DATA)
    with open(file_path, "w") as f:
        json.dump(data, f)


def get_user_data(data: dict, user_id):
    return data.get(user_id, {
        "rating": 0,
        "times_all": 0,
        "times_month": 0,
        "date": "0001-01-01"
    })


def get_reply(context):
    group_id = str(context['group_id'])

    from datetime import datetime, date
    import random
    data = load_data(group_id)

    sender = context['sender']
    user_id = str(sender['user_id'])
    nickname = sender['nickname']

    user_data = get_user_data(data, user_id)

    today = datetime.strptime(str(date.today()), '%Y-%m-%d')
    last_day = datetime.strptime(user_data['date'], '%Y-%m-%d')

    # 比较上次签到时间，今日已经签到
    if last_day >= today:
        return "%s今天已经签过到了！\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
            nickname, user_data['rating'], user_data['times_month'], user_data['times_all'])

    # 清零上个月
    if last_day.month != today.month or last_day.year != today.year:
        user_data['times_month'] = 0

    # 签到
    delta = random.randint(10, 50-datetime.now().hour)
    user_data['rating'] += delta
    user_data['times_month'] += 1
    user_data['times_all'] += 1
    user_data['date'] = str(date.today())
    data[user_id] = user_data
    save_data(data, group_id)
    return "给%s签到成功了！\n积分增加：%d\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
        nickname, delta, user_data['rating'], user_data['times_month'], user_data['times_all'])
