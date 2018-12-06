#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from global_vars import config
def get_reply(context):
    data = {}
    file_path=config.ATTENDANCE_DATA+"group_data.json"
    import os,json,random
    
    # 文件不存在，建立文件夹
    if not os.path.exists(config.ATTENDANCE_DATA):
        os.makedirs(config.ATTENDANCE_DATA)

    # 读取json文件
    if os.access(file_path, os.F_OK):
        with open(file_path,"r") as f:
            data=json.load(f)
    
    group_id = str(context['group_id'])
    sender = context['sender']
    user_id= str(sender['user_id'])
    nickname = sender['nickname']

    # 群不在字典中
    if group_id not in data.keys():
        data[group_id] = {}

    # 发件人不在群字典中
    if user_id not in data[group_id].keys():
        data[group_id][user_id]={
            "rating" : 0,
            "times_all" : 0,
            "times_month" : 0,
            "date" : "0001-01-01"
        }

    from datetime import datetime,date
    today = datetime.strptime(str(date.today()),'%Y-%m-%d')
    last_day = datetime.strptime(data[group_id][user_id]['date'],'%Y-%m-%d')
    
    
    #比较上次签到时间，今日已经签到
    if last_day >= today : 
        return "%s今天已经签过到了！\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
            nickname,data[group_id][user_id]['rating'],data[group_id][user_id]['times_month'],data[group_id][user_id]['times_all'])

    # 清零上个月
    if last_day.month!=today.month or last_day.year!=today.year:
        data[group_id][user_id]['times_month'] = 0
        
    #签到
    delta=random.randint(10,50-datetime.now().hour)
    data[group_id][user_id]['rating'] += delta
    data[group_id][user_id]['times_month'] += 1
    data[group_id][user_id]['times_all'] += 1
    data[group_id][user_id]['date'] = str(date.today())

    with open(file_path,"w") as f:
        json.dump(data,f)
    
    return "给%s签到成功了！\n积分增加：%d\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
        nickname,delta,data[group_id][user_id]['rating'],data[group_id][user_id]['times_month'],data[group_id][user_id]['times_all'])
