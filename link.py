#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
new Env('小迪 - 环境检测');
30 9 * * * link.py
enabled=false
"""
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from __utils import recursive_chmod, recursive_chown
from config import media_ext, full_link_mode, nas_mount_root_path, nas_slink_root_path, nas_strm_root_path, alist_root_url, xd_uid, xd_gid, xd_mod

mount_path = nas_mount_root_path
strm_path  = nas_strm_root_path
slink_path = nas_slink_root_path
alist_url  = alist_root_url

def write_to_file(content, save_strm_path):
    """
    创建 STRM 文件并写入内容。
    """
    parent_path = os.path.dirname(save_strm_path)
    os.makedirs(parent_path, exist_ok=True)
    with open(save_strm_path, 'w', encoding='utf-8') as f:
        f.write(content)
    recursive_chmod(parent_path, xd_mod)
    recursive_chown(parent_path, xd_uid, xd_gid)


def dl_to_path(source, dest):
    """
    下载非视频文件。
    """
    parent_path = os.path.dirname(dest)
    os.makedirs(parent_path, exist_ok=True)
    shutil.copy2(source, dest)
    recursive_chmod(parent_path, xd_mod)
    recursive_chown(parent_path, xd_uid, xd_gid)


def strm_file(file_path):
    """
    为指定文件创建 STRM 文件，非视频文件直接下载。
    """
    # 文件 STRM 路径，视频格式
    save_video_path = file_path.replace(mount_path, strm_path)
    if os.path.splitext(file_path)[1][1:].lower() in media_ext:
        # 文件 Alist URL
        content = file_path.replace(mount_path, alist_url)
        # 文件 STRM 路径，STRM 格式
        save_strm_path  = f"{os.path.splitext(save_video_path)[0]}.strm"
        if os.path.exists(save_strm_path):
            print("已存在，skip")
            return True
        print(f"视频 - {save_strm_path}")
        # 创建 STRM 文件
        write_to_file(content, save_strm_path)
    else:
        if os.path.exists(save_video_path):
            return True
        print(f"元数据 - {file_path}")
        # 下载非视频文件
        dl_to_path(file_path, save_video_path)


def strm_folder(folder_path):
    """
    为指定目录创建 STRM 文件，非视频文件直接下载。
    """
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            # 文件路径
            file_path = os.path.join(root, f)
            strm_file(file_path)


def slink_folder(folder_path):
    """
    为指定目录创建 SLINK 文件，非视频文件直接下载。
    """
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            # 文件路径
            file_path = os.path.join(root, f)
            slink_file(file_path)


def slink_file(file_path):
    """
    为指定文件创建 SLINK 文件，非视频文件直接下载。
    """
    root = os.path.dirname(file_path)
    # 文件 SLINK 路径，视频格式
    save_slink_path = file_path.replace(mount_path, slink_path)
    if os.path.exists(save_slink_path):
        print("已存在，skip")
        return True
    if os.path.splitext(file_path)[1][1:].lower() in media_ext:
        print(f"视频 - {save_slink_path}")
        # 创建 SLINK 文件
        parent_path = root.replace(mount_path, slink_path)
        os.makedirs(parent_path, exist_ok=True)
        try:
            os.symlink(file_path, save_slink_path)
        except FileNotFoundError as e:
            print(f"网盘文件不存在：{e}")
    else:
        if os.path.exists(save_slink_path):
            return True
        print(f"元数据 - {file_path}")
        # 下载非视频文件
        dl_to_path(file_path, save_slink_path)


def cd2_slink(self, file_mount_path, file_slink_path, file_ext):
    count = 0
    if file_ext in media_ext:
        if os.path.exists(file_slink_path):
            print("已存在，skip")
            return 0
        print(f"视频 - {file_slink_path}")
        parent_path = os.path.dirname(file_slink_path)
        os.makedirs(parent_path, exist_ok=True)
        try:
            os.symlink(file_mount_path, file_slink_path)
        except FileNotFoundError as e:
            print(f"网盘文件不存在：{e}")
        count += 1
        return count
    else:
        if os.path.exists(save_slink_path):
            return 0
        print(f"元数据 - {file_mount_path}")
        dl_to_path(file_mount_path, file_slink_path)
        return 0


def cd2_strm(self, file_mount_path, file_strm_path, file_ext):
    count = 0
    if file_ext in media_ext:
        # 文件 Alist URL
        content = file_path.replace(file_mount_path, alist_url)
        # 文件 STRM 路径，STRM 格式
        save_strm_path  = f"{os.path.splitext(file_strm_path)[0]}.strm"
        if os.path.exists(save_strm_path):
            print("已存在，skip")
            return 0
        print(f"视频 - {save_strm_path}")
        # 创建 STRM 文件
        write_to_file(content, save_strm_path)
        count += 1
        return count
    else:
        if os.path.exists(file_strm_path):
            return 0
        print(f"元数据 - {file_mount_path}")
        # 下载非视频文件
        dl_to_path(file_mount_path, file_strm_path)
        return 0






if __name__ == "__main__":
    if full_link_mode == "strm":
        with ThreadPoolExecutor(max_workers=10) as executor:
            r = executor.submit(strm_folder, mount_path)
    elif full_link_mode == "slink":
        with ThreadPoolExecutor(max_workers=10) as executor:
            r = executor.submit(slink_folder, mount_path)
    elif full_link_mode == "both":
        with ThreadPoolExecutor(max_workers=10) as executor:
            r = executor.submit(strm_folder, mount_path)
        with ThreadPoolExecutor(max_workers=10) as executor:
            r = executor.submit(slink_folder, mount_path)
    else:
        print("链接模式变量 full_link_mode 未设置！可选值：strm、slink、both")
