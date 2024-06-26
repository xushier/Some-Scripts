#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created By Xiaodi
小迪同学:
https://github.com/xushier/HD-Icons
https://space.bilibili.com/32313260
2024/06/19
"""

import re
from qbittorrent import Client

xd_qb_url = "http://"
xd_qb_usr = ""
xd_qb_pwd = ""


class Qb:
    def __init__(self, qb_url=xd_qb_url, qb_usr=xd_qb_usr, qb_pwd=xd_qb_pwd):
        self.qb_url = qb_url
        self.qb_usr = qb_usr
        self.qb_pwd = qb_pwd
        self.qb     = Client(self.qb_url, verify=False)
        self.qb.login(self.qb_usr, self.qb_pwd)

        self.categories = self.qb_categories()
        self.torrents   = self.qb_torrents(stat='seeding')

    def qb_create_category(self, new_category):
        """
        创建 Qbittirrent 客户端的分类。

        """
        new_category = new_category.replace(" ", "").lower()
        return self.qb.create_category(new_category)

    def qb_set_category(self, torrent_hash, category):
        """
        设置 Qbittirrent 客户端的分类。

        """
        return self.qb.set_category(torrent_hash, category)
    
    def qb_categories(self):
        """
        获取 Qbittirrent 客户端的分类。

        """
        categories = self.qb._post("torrents/categories", data="").keys()
        return list(categories)
    
    def qb_torrents(self, stat="seeding"):
        """
        获取 Qbittirrent 指定种子。

        """
        return self.qb.torrents(filter=stat)

    def delete_true(self, infohash_list):
        """
        删除 Qbittirrent 指定种子及文件。

        """
        return self.qb.delete_permanently(infohash_list)

    def get_trackers(self, infohash):
        """
        获取指定种子 Tracker 信息。
        """
        return self.qb.get_torrent_trackers(infohash)


    def can_delete(self):
        """
        删除满足条件的种子。

        """
        print("----------删除可删种子----------")
        ts = self.qb_torrents()
        # print(ts)
        hash_list = set()
        for t in ts:
            if "可删" in t['category']:
                name = t['category'].split("-")[3]
                seeding_time = t['seeding_time'] // 3600
                size = t['size'] // 1073741824
                if "chdbits" in t['tracker'] or "chdbits" in t['magnet_uri'] or "CHD" in t['tags']:
                    if seeding_time <= 8640:
                        # print(f"彩虹岛，{t['tags']}，{t['category']}, 做种 {seeding_time} 小时，不足 6 天，暂不删除")
                        continue
                if re.search(r'^[a-zA-Z]$', name) and not re.search(r'[\u4e00-\u9fff]', name):
                    print(f"片名：{name}，可能识别错误，暂不删除")
                    continue
                print(f"可删, {size} GB, 做种 {seeding_time} 小时, {t['tags']}, {t['category']}")
                hash_list.add(t['hash'])
        count = len(hash_list)
        if count:
            self.delete_true(list(hash_list))
            print(f"本次删除 {count} 个可删除种子")
            return count
        else:
            print("本次运行没有检测到可以删除的种子。")
            return 0


    def delete_error(self):
        """
        删除已失效的种子。

        """
        print("\n----------删除失效种子----------")
        ts = self.qb_torrents(stat='downloading')
        # print(ts)
        hash_list = set()
        for t in ts:
            infohash = t['hash']
            progress = round(t['progress'] * 100, 2)
            infotracker = self.get_trackers(infohash)[-1]['msg']
            if 'exist' in infotracker or 'anned' in infotracker or 'register' in infotracker:
                size = t['size'] // 1073741824
                print(f"种子已失效, {size} GB, 进度：{progress} %, 服务器信息：{infotracker}")
                hash_list.add(infohash)
        count = len(hash_list)
        if count:
            self.delete_true(list(hash_list))
            print(f"本次删除 {count} 个可删除种子")
            return count
        else:
            print("本次运行没有检测到已失效的种子。")
            return 0



s = Qb()
s.can_delete()
s.delete_error()

