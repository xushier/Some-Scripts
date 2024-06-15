#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""变量
    export cd2_url=""
    export cd2_usr=""
    export cd2_pwd=""
    export save_path=""
    export mount_path=""
    export add_mode=""
    export clean_mode=""
"""

"""通知参数

    BARK_PUSH         # bark IP 或设备码，例：https://api.day.app/DxHcxxxxxRxxxxxxcm/
    BARK_ARCHIVE      # bark 推送是否存档
    BARK_GROUP        # bark 推送分组
    BARK_SOUND        # bark 推送声音
    BARK_ICON         # bark 推送图标

    DD_BOT_SECRET     # 钉钉机器人的 DD_BOT_SECRET
    DD_BOT_TOKEN      # 钉钉机器人的 DD_BOT_TOKEN

    FSKEY             # 飞书机器人的 FSKEY

    GOBOT_URL         # go-cqhttp
                        # 推送到个人QQ：http://127.0.0.1/send_private_msg
                        # 群：http://127.0.0.1/send_group_msg
    GOBOT_QQ          # go-cqhttp 的推送群或用户
                        # GOBOT_URL 设置 /send_private_msg 时填入 user_id=个人QQ
                        #               /send_group_msg   时填入 group_id=QQ群
    GOBOT_TOKEN       # go-cqhttp 的 access_token

    GOTIFY_URL        # gotify地址,如https://push.example.de:8080
    GOTIFY_TOKEN      # gotify的消息应用token
    GOTIFY_PRIORITY   # 推送消息优先级,默认为0

    IGOT_PUSH_KEY     # iGot 聚合推送的 IGOT_PUSH_KEY

    PUSH_KEY          # server 酱的 PUSH_KEY，兼容旧版与 Turbo 版

    DEER_KEY          # PushDeer 的 PUSHDEER_KEY

    PUSH_PLUS_TOKEN   # push+ 微信推送的用户令牌
    PUSH_PLUS_USER    # push+ 微信推送的群组编码

    QMSG_KEY          # qmsg 酱的 QMSG_KEY
    QMSG_TYPE         # qmsg 酱的 QMSG_TYPE

    QYWX_AM           # 企业微信应用

    QYWX_KEY          # 企业微信机器人

    TG_BOT_TOKEN      # tg 机器人的 TG_BOT_TOKEN，例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
    TG_USER_ID        # tg 机器人的 TG_USER_ID，例：1434078534
    TG_API_HOST       # tg 代理 api
    TG_PROXY_AUTH     # tg 代理认证参数
    TG_PROXY_HOST     # tg 机器人的 TG_PROXY_HOST
    TG_PROXY_PORT     # tg 机器人的 TG_PROXY_PORT
"""

import os, sys

sht_config = {
    'cd2_url': '',
    'cd2_usr': '',
    'cd2_pwd': '',
    'save_path': '',
    'mount_path': '',
    'add_mode': '',
    'clean_mode': '',
    'account_id': ''
}

for c in sht_config:
    v = os.getenv(c)
    if c == "cd2_url" and  not v.startswith("http"):
        raise KeyError(f"{c} 输入可能错误，需以 http 或者 https 开头！")
    if c == "save_path" and  not v.startswith("/115"):
        raise KeyError(f"{c} 输入可能错误，115 网盘是以 /115 开头！")
    if c == "add_mode" and ( v == "1" or v == None ):
        add, and_clean = 1, 1
        continue
    if c == "add_mode" and v == "2":
        add, and_clean = 1, 0
        continue
    if c == "clean_mode" and v == "1":
        all_clean, part_clean = 1, 0
        continue
    if c == "clean_mode" and v == "2":
        all_clean, part_clean = 0, 1
        continue
    if c == "clean_mode" and v == None:
        all_clean, part_clean = 0, 0
        continue
    if c == "account_id" and v == None:
        sht_config[c] = False
        continue
    if v:
        sht_config[c] = v
    else:
        raise KeyError(f"{c} 变量未设置！")


if len(sys.argv) == 2:
    target_date, target_category = sys.argv[1], ""
elif len(sys.argv) == 3:
    target_date, target_category = sys.argv[1], sys.argv[2]
else:
    target_date, target_category = "", ""


category_dict  = {
    '4k_video': '4K',
    'anime_originate': '动漫',
    'asia_codeless_originate': '亚洲无码',
    'asia_mosaic_originate': '亚洲有码',
    'domestic_original': '国产原创',
    'EU_US_no_mosaic': '欧美无码',
    'hd_chinese_subtitles': '中文字幕',
    'vegan_with_mosaic': '素人有码',
    'vr_video': 'VR',
    'three_levels_photo': '三级'
}

for l in category_dict:
    m = os.getenv(l)
    if m:
        category_dict[l] = m
if os.getenv("uhd_video"):
    category_dict['4k_video'] = os.getenv("uhd_video")


clean_min_size = 100
