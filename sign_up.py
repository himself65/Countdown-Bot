#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
def get_reply(context):
    from global_vars import config
    Data = {}
    file_path=config.ATTENDANCE_DATA+"group_data.json"
    import os,json,random
    
    # 文件不存在，建立文件夹
    if not os.path.exists(config.ATTENDANCE_DATA):
        os.makedirs(config.ATTENDANCE_DATA)

    # json不存在，建立空文件
    if not os.access(file_path, os.F_OK):
        with open(file_path,'w') as f:
            json.dump(Data,f)

    # 读取json文件
    with open(file_path,"r") as f:
        Data=json.load(f)
    
    group_id = str(context['group_id'])
    sender = context['sender']
    user_id= str(sender['user_id'])
    nickname = sender['nickname']

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

    from datetime import datetime,date
    today = datetime.strptime(str(date.today()),'%Y-%m-%d')
    last_day = datetime.strptime(Data[group_id][user_id]['date'],'%Y-%m-%d')
    
    
    #比较上次签到时间，今日已经签到
    if last_day >= today : 
        return "%s今天已经签过到了！\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
            nickname,Data[group_id][user_id]['rating'],Data[group_id][user_id]['times_month'],Data[group_id][user_id]['times_all'])

    # 清零上个月
    if last_day.month!=today.month or last_day.year!=today.year:
        Data[group_id][user_id]['times_month'] = 0
        
    #签到
    delta=random.randint(10,50-datetime.now().hour)
    Data[group_id][user_id]['rating'] += delta
    Data[group_id][user_id]['times_month'] += 1
    Data[group_id][user_id]['times_all'] += 1
    Data[group_id][user_id]['date'] = str(date.today())

    with open(file_path,"w") as f:
        json.dump(Data,f)
    
    return "给%s签到成功了！\n积分增加：%d\n当前积分：%d\n本月签到次数：%d\n累计群签到次数：%d" % (
        nickname,delta,Data[group_id][user_id]['rating'],Data[group_id][user_id]['times_month'],Data[group_id][user_id]['times_all'])
