#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from global_vars import config

Path=config.ATTENDANCE_DATA+"group_data.json"

import json,time

Data = {}

def get_reply(context):

    import os
    # json文件不存在，建立文件
    if not os.access(Path, os.F_OK):
        os.makedirs(JsonFilePath)
    # 读取json文件
    FILE = open(JsonFilePath,"r")
    Data=json.load(load_f)
    FILE.close()
    
    group_id = context['group_id']
    sender = context['sender']
    user_id= sender['user_id']
    nikename = sender['nickname']

    # 群不在字典中
    if group_id not in Data.keys():
        Data[group_id] = {}

    # 发件人不在群字典中
    if user_id not in Data[group_id].keys():
        Data[group_id][user_id]={
            "rating" : 0,
            "times_all" : 0,
            "times_month" : 0,
            "date" : "0001-01-01"
        }

    from datatime import datetime,date
    today = datetime.strptime(str(date.today()),'%Y-%m-%d')
    last_day = datetime.strptime(Data[group_id][user_id]['date'],'%Y-%m-%d')
    
    
    #比较上次签到时间，今日已经签到
    if last_day >= today : 
        return "%s今天已经签过到了！\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
            nickname,Date[group_id][user_id]['rating'],Data[group_id][user_id]['times_month'],Data[group_id][user_id]['times_all'])

    # 清零上个月
    if lats_day.month!=today.month or last_day.year!=today.year:
        Data[group_id][user_id]['times_month'] = 0
        
    #签到
    delta=rand(1,30-datetime.now().hour)
    Date[group_id][user_id]['rating'] += dalta
    Data[group_id][user_id]['times_month'] += 1
    Data[group_id][user_id]['times_all'] += 1
    Data[group_id][user_id]['date'] = "%d-%d-%d" % ()

    FILE = open(JsonFilePath,"w")
    json.dump(Data,FILE)
    FILE.close()
    
    return "给%s签到成功了！\n积分增加：%d\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
        nickname,delta,Date[group_id][user_id]['rating'],Data[group_id][user_id]['times_month'],Data[group_id][user_id]['times_all'])
    
