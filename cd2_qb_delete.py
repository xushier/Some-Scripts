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
    
    def can_delete(self):
        """
        删除满足条件的种子。

        """
        ts = self.qb_torrents()
        hash_list = set()
        for t in ts:
            if "可删" in t['category']:
                name = t['category'].split("-")[3]
                seeding_time = t['seeding_time'] // 3600
                if "chdbits" in t['tracker'] or "chdbits" in t['magnet_uri'] or "CHD" in t['tags']:
                    if seeding_time <= 8640:
                        print(f"彩虹岛，{t['category']}, 做种 {seeding_time} 小时，不足 6 天，暂不删除")
                        continue
                if re.search(r'^[a-zA-Z]$', name) and not re.search(r'[\u4e00-\u9fff]', name):
                    print(f"片名：{name}，可能识别错误，暂不删除")
                    continue
                print(f"可删, {t['category']}")
                hash_list.add(t['hash'])
        if len(hash_list):
            self.delete_true(list(hash_list))
            return len(hash_list)


s = Qb().can_delete()
print(f"本次删除 {s} 个")
