# -*- coding: utf-8 -*-
"""
Created By Xiaodi
小迪同学:
https://github.com/xushier/HD-Icons
https://space.bilibili.com/32313260
2024/02/12
"""


'''
export cd2_url=""
export cd2_usr=""
export cd2_pwd=""
export save_path=""
export QYWX=""
'''

import time
import logging
import logging.handlers
import os
import sys
import re
import requests
import json
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from clouddrive import CloudDriveClient
from CloudDrive_pb2 import AddOfflineFileRequest


sht_ql_config = {
    'cd2_url': '',
    'cd2_usr': '',
    'cd2_pwd': '',
    'save_path': '',
    'QYWX': ''
}

for c in sht_ql_config:
    if os.getenv(c):
        v = os.getenv(c)
        sht_ql_config[c] = v
    else:
        raise KeyError(f"{c} 未设置！")


class AddSht:

    def __init__(self, target_date = "", target_category = "", clean = False):
        self.mongodb = MongoClient("mongodb+srv://readonly:cS9NSuiJ1ebHnUL0@cluster0.8mosa.mongodb.net/Cluster0?retryWrites=true&w=majority")
        try:
            self.db = self.mongodb["sehuatang"]
            self.categories = self.db.list_collection_names()
        except errors.OperationFailure as e:
            # 捕获 OperationFailure 异常
            if 'bad auth' in str(e):
                # 检查错误消息是否包含 "bad auth"
                print("认证失败，错误信息:", e)
            else:
                # 处理其他类型的 OperationFailure 异常
                print("操作失败，错误信息:", e)
            self.mongodb.close()
            sys.exit("数据库连接错误，程序退出！")
        except Exception as e:
            # 捕获其他所有异常
            print("发生了其他错误:", e)
            self.mongodb.close()
            sys.exit("数据库连接错误，程序退出！")

        self.cd2_url        = sht_ql_config['cd2_url']
        self.cd2_usr        = sht_ql_config['cd2_usr']
        self.cd2_pwd        = sht_ql_config['cd2_pwd']
        self.save_path      = sht_ql_config['save_path']
        self.cd2            = CloudDriveClient(self.cd2_url, self.cd2_usr, self.cd2_pwd)
        self.notify         = Send_Notify()
        self.notify_content = []
        self.clean          = clean

        self.category_dict   = {
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

        # 日志系统的初始化和配置
        log_path     = "sht-log"
        max_log_size = 2 * 1024 * 1024
        back_count   = 10
        os.makedirs(log_path, exist_ok=True)
        self.log_file = f"{log_path}/{str(datetime.now().date())}.log"
        handler       = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=max_log_size, backupCount=back_count)
        formatter     = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger('sht')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

        self.magnets_path    = "sht-magnets"
        self.target_date     = self.__init_date__(target_date)
        self.category        = target_category
        self.target_category = self.__category_judge__()
        self.magnets_dict    = self.__get_magnet_list__()

        self.filter_file = ["*.exe", "*.mht", "*.mhtml", "*.rar", "*. c o m*.mp4", "*.htm", "*.html", "*.txt", "*.url", "*.jpg", "*.png", "*.docx", "*.doc", "*.zip", "*.apk", "uur76.mp4", "*最 新*.mp4", "*更 新*.mp4", "*直 播*.mp4", "*.nfo"]

    def __is_valid_date__(self, date_str):
        """
        检查字符串是否为有效的日期格式。
        """
        try:
            # 尝试将字符串解析为日期对象
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # 检查日期是否合法
            if date_obj.year < 1 or date_obj.year > 9999:
                return False
            if date_obj.month < 1 or date_obj.month > 12:
                return False
            if date_obj.day < 1 or date_obj.day > 31:
                return False
            # 对于2月，检查是否是闰年
            if date_obj.month == 2:
                if date_obj.day == 29:
                    # 闰年的条件是年份能被4整除但不能被100整除，或者能被400整除
                    if (date_obj.year % 4 == 0 and date_obj.year % 100 != 0) or (date_obj.year % 400 == 0):
                        return True
                    else:
                        return False
                else:
                    return True
            # 对于其他月份，检查日期是否合法
            max_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if date_obj.day <= max_day[date_obj.month - 1]:
                return True
            else:
                return False
        except ValueError:
            # 如果解析失败，说明日期格式不正确
            return False

    def __date_judge__(self, date_str):
        """
        判断日期是否合法。
        """
        if not date_str:
            date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if self.__is_valid_date__(date_str):
            return date_str
        else:
            raise ValueError(f"日期 {date_str} 输入错误，请重新输入！")

    def __parse_date__(self, date_str):
        """解析日期字符串为 datetime 对象"""
        return datetime.strptime(date_str, '%Y-%m-%d')

    def __init_date__(self, target_date):
        """初始化日期范围"""
        if "," in target_date:
            start_str, end_str = target_date.split(',')
            start_str = self.__date_judge__(start_str)
            end_str   = self.__date_judge__(end_str)
            # 解析起始和结束日期为日期对象
            start_date = self.__parse_date__(start_str)
            end_date   = self.__parse_date__(end_str)
            return start_date, end_date
        else:
            # 如果没有逗号，则假设第二个参数是一个单独的日期
            range_date = self.__parse_date__(self.__date_judge__(target_date))
            return range_date

    def __is_date_in_range_or_equal__(self, date_str):
        """判断日期是否在指定范围内或是否相等"""
        # 解析第一个参数为日期对象
        date_str = self.__date_judge__(date_str)
        date = self.__parse_date__(date_str)

        # 尝试分割第二个参数，看是否有逗号分隔的日期范围
        if isinstance(self.target_date, tuple):
            # 检查日期是否在范围内或是否等于起始日期或结束日期
            if self.target_date[0] <= date <= self.target_date[1]:
                return True
        else:
            # 检查日期是否相等
            if date == self.target_date:
                return True

        # 如果以上条件都不满足，则返回 False
        return False

    def __is_in_category_dict__(self, category_name):
        """
        判断输入的分类名称是否在 category_dict 中。
        """
        categories = set(self.category_dict.values())
        if isinstance(category_name, set):
            for c in category_name:
                if c not in categories:
                    raise ValueError(f"{category_name} 输入错误，请检查！")
            return True
        if isinstance(category_name, str):
            if category_name not in categories:
                raise ValueError(f"{category_name} 输入错误，请检查！")
            return True

    def __category_judge__(self):
        """
        分类判断。
        """
        if not self.category:
            categories = set(self.category_dict.values())
        elif "-" in self.category:
            categories = set(self.category.split(","))
        else:
            categories = [self.category]
        self.__is_in_category_dict__(categories)
        return categories

    def __save_info_to_file__(self, magnets_dict):
        """
        保存信息到文件。
        """
        file_path = f"{self.magnets_path}/{self.target_date}.txt"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            for category_zh, magnets_list in magnets_dict.items():
                f.write(f"\n{category_zh}\n")
                for magnet in magnets_list:
                    f.write(f"{magnet}\n")

    def __get_magnet_list__(self):
        """
        获取目标日期的资源。
        """
        magnets_dict = {}
        for category_zh in self.target_category:
            for key, value in self.category_dict.items():
                if category_zh == value:
                    category = key
                    break
            magnets_list = set()
            target_table = self.db[category]
            cursor = target_table.find().sort("date", 1)
            for item in cursor:
                if self.__is_date_in_range_or_equal__(item["date"]):
                    magnets_list.add(item["magnet"])
            magnets_dict[category_zh] = magnets_list
        self.__save_info_to_file__(magnets_dict)
        return magnets_dict

    def cd2_add(self):
        """
        添加种子到 115。
        """
        if isinstance(self.target_date, tuple):
            d1 = self.target_date[0].strftime('%Y-%m-%d')
            d2 = self.target_date[1].strftime('%Y-%m-%d')
            d = f"{d1}-{d2}"
        else:
            d = self.target_date.strftime('%Y-%m-%d')
        self.notify_content.append(f"日期：{d}")
        self.logger.info(f"日期：{d}")
        print(f"日期：{d}")
        count = 0
        if self.magnets_dict:
            for key, value in self.magnets_dict.items():
                category_name = key
                torrent_str   = "\n".join(value)
                save_path = f"{self.save_path}/SHT/{category_name}/{d}"
                self.cd2.fs.makedirs(save_path, exist_ok=True)
                self.cd2.AddOfflineFiles(AddOfflineFileRequest(urls=torrent_str, toFolder=save_path))
                if len(self.magnets_dict[key]):
                    print(f"{category_name} 添加完成，共 {len(self.magnets_dict[key])} 个")
                    self.notify_content.append(f"{category_name} 共添加 {len(self.magnets_dict[key])} 个资源")
                self.logger.info(f"{category_name} 共添加 {len(self.magnets_dict[key])} 个资源")
                if self.clean:
                    self.clean_ads(save_path)
                time.sleep(2)
        else:
            print("本次没有新资源")

    def clean_ads(self, path):
        """
        清理垃圾文件。
        """
        self.cd2.fs.chdir(path)
        print(f"\n开始清理")
        count = 0
        for info in self.filter_file:
            for path in self.cd2.fs.rglob(info):
                print(path)
                count += 1
                try:
                    self.cd2.fs.remove(path)
                except OSError as e:
                    print("遇到错误：", e)
                except FileNotFoundError as e:
                    print("遇到错误：", e)
                except Exception as e:
                    print("遇到错误：", e)
            time.sleep(3)
        self.logger.info(f"清理完成，共清理 {count} 个垃圾文件")
        self.notify_content.append(f"清理完成，共清理 {count} 个垃圾文件")

    def notify_wechat(self):
        """
        微信通知。
        """
        if self.notify_content:
            title   = f"【啬骅自动化】"
            content = "\n".join(self.notify_content)
            self.notify.wechat(title, content)



class Send_Notify(object):

    def __init__(self) -> None:
        self.pushplus_url = 'http://www.pushplus.plus/send?' + 'token='

    def pushplus(self, title:str, content:str) -> None:
        if not sht_ql__config.get("PUSH_PLUS_TOKEN"):
            print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
            return
        print("PUSHPLUS 服务启动")

        pushplus_headers = {'Content-Type':'application/json'}
        pushplus_req = requests.get(self.pushplus_url + sht_ql__config.get("PUSH_PLUS_TOKEN") +'&title='+title+'&content='+content,headers=pushplus_headers)
        if pushplus_req.status_code == 200:
            print("通知发送成功！")
        else:
            print("通知发送失败！")

    def wechat(self, title: str, content: str) -> None:
        """
        通过 企业微信 APP 推送消息。
        """
        if not sht_ql_config.get("QYWX"):
            print("QYWX 未设置!!\n取消推送")
            return
        QYWX_AY = re.split(",", sht_ql_config.get("QYWX"))
        if 4 < len(QYWX_AY) > 5:
            print("QYWX 设置错误!!\n取消推送")
            return
        # print("企业微信 APP 服务启动")

        corpid     = QYWX_AY[0]
        corpsecret = QYWX_AY[1]
        touser     = QYWX_AY[2]
        agentid    = QYWX_AY[3]
        try:
            media_id = QYWX_AY[4]
        except IndexError:
            media_id = ""
        wx = We_Com(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message  = title + "\n\n" + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)

        if response == "ok":
            # print("企业微信推送成功！")
            pass
        else:
            print("企业微信推送失败！错误信息如下：\n", response)

        def iyuu(self, title:str, content:str) -> None:
            pass

class We_Com(object):
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID     = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID    = agentid

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {
            "corpid": self.CORPID,
            "corpsecret": self.CORPSECRET,
        }
        req  = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace("\n", "<br/>"),
                        "digest": message,
                    }
                ]
            },
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        target_date = sys.argv[1]
    elif len(sys.argv) == 3:
        target_date     = sys.argv[1]
        target_category = sys.argv[2]
    else:
        target_date     = ""
        target_category = ""
    sh = AddSht(target_date, target_category)
    sh.logger.info(f"###############本次执行开始###############")
    sh.cd2_add()
    sh.logger.info(f"+++++++++++++++++++++++++++++++++++++++++")
    sh.notify_wechat()
    sh.logger.info(f"###############本次执行结束###############\n\n")
