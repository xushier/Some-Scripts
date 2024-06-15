#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created By Xiaodi
小迪同学:
https://github.com/xushier/HD-Icons
https://space.bilibili.com/32313260
2024/02/12
"""

from __initial_modules import *
from __initial_vars import *

log_path     = "clean-log"
max_log_size = 2 * 1024 * 1024
back_count   = 10
os.makedirs(log_path, exist_ok=True)
log_file     = f"{log_path}/{str(datetime.now().date())}.log"
handler      = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=back_count)
formatter    = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('clean')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_writer(log_queue):
    while True:
        try:
            log_entry = log_queue.get(block=True)
            if log_entry is None:
                break
            logger.info(log_entry)
        except Exception as e:
            if str(e) != 'Empty':
                raise

def clean_ads(log_queue, clean_path = "", min_size_mb = ""):
    """
    清理垃圾文件。
    """
    print(f"开始清理 {clean_path}")
    if not min_size_mb:
        min_size_mb = clean_min_size
    count = 0
    min_size_bytes  = min_size_mb * 1024 * 1024
    for root, dirs, files in os.walk(clean_path, topdown=False):
        for f in files:
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            if file_size < min_size_bytes:
                try:
                    count += 1
                    os.remove(file_path)
                    log_queue.put(f"删除文件{count}: {file_path}")
                except Exception as e:
                    log_queue.put(f"删除错误：{file_path}: {e}")
                    print(f"删除错误：{file_path}: {e}")
        if not dirs and not files:
            try:
                folder_time = os.stat(root).st_mtime
                if time.time() - folder_time > 172800:
                    count += 1
                    os.rmdir(root)
                    log_queue.put(f"删除文件夹{count}: {root}")
                # count += 1
                # os.rmdir(root)
                # log_queue.put(f"删除文件夹{count}: {root}")
            except Exception as e:
                log_queue.put(f"删除错误：{root}: {e}")
    return count

def clean_all(clean_path = sht_config['mount_path'] + "/SHT", min_size_mb = clean_min_size):
    log_queue  = Queue()
    log_thread = Thread(target=log_writer, args=(log_queue,))
    log_thread.start()
    with ThreadPoolExecutor(max_workers=12) as executor:
        r = executor.submit(clean_ads, log_queue, clean_path, min_size_mb)
    log_queue.put(None)
    log_thread.join()
    return r.result()


def clean_part():
    date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    d   = datetime.strptime(date_str, '%Y-%m-%d')
    d1t = d - timedelta(days=1)
    d2t = d - timedelta(days=2)
    d3t = d - timedelta(days=3)
    d0  = d.strftime('%Y-%m-%d')
    d1  = d1t.strftime('%Y-%m-%d')
    d2  = d2t.strftime('%Y-%m-%d')
    d3  = d3t.strftime('%Y-%m-%d')
    content = []
    mount_path = sht_config['mount_path']
    allc = 0
    for s in category_dict.values():
        path_list = [f"{mount_path}/SHT/{s}/{d0}", f"{mount_path}/SHT/{s}/{d1}", f"{mount_path}/SHT/{s}/{d2}", f"{mount_path}/SHT/{s}/{d3}"]
        total = 0
        for p in path_list:
            if os.path.exists(p):
                total += clean_all(p)
        allc += total
        content.append(f"{total} 个 {s}")
        logger.info(f"清理 {total} 个 {s}")
    content.append(f"共 {total} 个")
    logger.info(f"共 {total} 个")
    return "\n".join(content)


if __name__ == "__main__":
    if all_clean:
        print(f"开始全量清理\n")
        print("注：为避免日志太多青龙卡死，此处不输出日志，日志保存于 clean-log 文件夹，不要看到长时间无输出就停止任务。")
        count = clean_all()
        send(f"大姐姐洗澡器", f"大扫除，共洗去 {count} 个")
        print(f"大扫除，共洗去 {count} 个")
    else:
        print(f"未启用全量清理，不执行\n")
    if part_clean:
        print(f"开始循环清理\n")
        content = clean_part()
        send(f"大姐姐洗澡器", content)
    else:
        print(f"未启用循环清理，不执行\n")
