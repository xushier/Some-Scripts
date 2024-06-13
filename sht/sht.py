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
from __notify_templates import add_content
from Clean import clean_all


class AddSht:
    def __init__(self, target_date = target_date, target_category = target_category):
        self.mount_path = sht_config['mount_path']

        # 日志系统的初始化和配置
        log_path     = "sht-log"
        max_log_size = 2 * 1048576
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

        self.cd2_url   = sht_config['cd2_url']
        self.cd2_usr   = sht_config['cd2_usr']
        self.cd2_pwd   = sht_config['cd2_pwd']
        self.save_path = sht_config['save_path']
        self.cd2       = CloudDriveClient(self.cd2_url, self.cd2_usr, self.cd2_pwd)
        self.cd2_info  = self.cd2_info()

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
                print("操作失败，错误信息:", e)
            self.mongodb.close()
            sys.exit("数据库连接错误，程序退出！")
        except Exception as e:
            print("发生了其他错误:", e)
            self.mongodb.close()
            sys.exit("数据库连接错误，程序退出！")

        self.magnets_path    = "sht-magnets"
        self.target_date     = self.__init_date__(target_date)
        self.category        = target_category
        self.target_category = self.__category_judge__()
        self.magnets_dict    = self.__get_magnet_list__()

    def cd2_info(self):
        """
        获取 CD2 相关信息。
        """
        info = {}
        mount_info = self.cd2.GetMountPoints()
        mounted    = mount_info.mountPoints[0].isMounted
        if not mounted:
            print("CloudDrive2 掉挂载！退出脚本")
            send("CD2 掉挂载！", "如题")
            sys.exit(1)

        tbyte = 1099511627776
        path  = "/" + sht_config['save_path'].split("/")[1]
        space = self.cd2.GetSpaceInfo(FileRequest(path = path))
        total_space = space.totalSpace // tbyte
        used_space  = space.usedSpace // tbyte
        free_space  = space.freeSpace // tbyte

        update_info = self.cd2.HasUpdate()
        hasUpdate   = update_info.hasUpdate
        newVersion  = update_info.newVersion
        updateLog   = update_info.description

        run_info    = self.cd2.GetRuntimeInfo()
        nowVersion  = run_info.productVersion.split(" ")[0]
        info['nowVersion'] = nowVersion

        if mounted:
            info['mount'] = "已挂载"
            info['used']  = f"{used_space} TB"
            info['free']  = f"{free_space} TB"
            info['nowVersion'] = nowVersion
        if hasUpdate:
            info['hasUpdate']  = "有新版本"
            info['newVersion'] = newVersion
            info['updateLog']  = updateLog
        else:
            info['hasUpdate']  = "无更新"
            info['newVersion'] = ""
            info['updateLog']  = ""
        
        return info


    def __is_valid_date__(self, date_str):
        """
        检查字符串是否为有效的日期格式。
        """
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
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
            if start_date <= end_date:
                return start_date, end_date
            else:
                raise KeyError(f"日期范围输入错误：{start_date} - {end_date}")
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
        return False


    def __is_in_category_dict__(self, category_name):
        """
        判断输入的分类名称是否在 category_dict 中。
        """
        categories = set(category_dict.values())
        if isinstance(category_name, (list, set)):
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
            categories = set(category_dict.values())
        elif "-" in self.category:
            categories = set(self.category.split("-"))
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
                for magnet in magnets_list[0]:
                    f.write(f"{magnet}\n")


    def __get_magnet_list__(self):
        """
        获取目标日期的资源。
        """
        magnets_dict = {}
        print("获取磁力链接···")
        for category_zh in category_dict.values():
            for key, value in category_dict.items():
                if category_zh == value:
                    category = key
                    break
            magnets_list = set()
            if category_zh in self.target_category:
                target_table = self.db[category]
                cursor = target_table.find().sort("date", 1)
                for item in cursor:
                    if self.__is_date_in_range_or_equal__(item["date"]) and item["magnet"].startswith('magnet'):
                        magnets_list.add(item["magnet"])
            magnets_dict[category_zh] = [magnets_list, category]
        print("记录磁力链接···")
        self.__save_info_to_file__(magnets_dict)
        return magnets_dict


    def cd2_add(self):
        """
        添加种子到 115。
        """
        notify_info = {}
        if isinstance(self.target_date, tuple):
            d1 = self.target_date[0].strftime('%Y-%m-%d')
            d2 = self.target_date[1].strftime('%Y-%m-%d')
            d = f"{d1}-{d2}"
        else:
            d = self.target_date.strftime('%Y-%m-%d')
        self.logger.info(f"日期：{d}")
        print(f"日期：{d}")
        if self.magnets_dict:
            for key, value in self.magnets_dict.items():
                category_name = key
                torrent_str   = "\n".join(value[0])
                save_path = f"{self.save_path}/SHT/{category_name}/{d}"
                self.cd2.fs.makedirs(save_path, exist_ok=True)
                try:
                    r = self.cd2.AddOfflineFiles(AddOfflineFileRequest(urls=torrent_str, toFolder=save_path))
                    if not r.success:
                        self.logger.info(f"添加离线失败，原因：{r.errorMessage}")
                except Exception as e:
                    print("捕获到异常，已忽略:", e)
                    continue
                print(f"{category_name}，共 {len(value[0])} 个")
                notify_info[value[1]] = [category_name, len(value[0])]
                if and_clean:
                    if len(self.magnets_dict[key]) > 0:
                        print("已添加离线，等待 2 秒···")
                        time.sleep(2)
                    d1t = self.__parse_date__(d) - timedelta(days=1)
                    d2t = self.__parse_date__(d) - timedelta(days=2)
                    d1  = d1t.strftime('%Y-%m-%d')
                    d2  = d2t.strftime('%Y-%m-%d')
                    path_list = [f"{self.mount_path}/SHT/{category_name}/{d}", f"{self.mount_path}/SHT/{category_name}/{d1}", f"{self.mount_path}/SHT/{category_name}/{d2}"]
                    total = 0
                    for p in path_list:
                        if os.path.exists(p):
                            total = total + clean_all(p)
                    print(f"循环清理：{total} 个\n")
                    self.logger.info(f"{len(value[0])} 个 {category_name}，清理：{total} 个")
                    notify_info[value[1]].append(total)
                else:
                    notify_info[value[1]].append("未启用")
            return notify_info, d
        else:
            print("本次没有新资源")


if __name__ == "__main__":
    if add:
        sh = AddSht()
        sh.logger.info(f"###############本次执行开始###############")
        info = sh.cd2_add()
        print(info)
        print(sh.cd2_info)
        info_data, total_add, total_clean = add_content(sh.cd2_info, info[0], info[1])
        digest = f"✅本次共添加 {total_add} 个，删除 {total_clean} 个。\n✅CD2 挂载正常。"
        send("大姐姐诱捕器", info_data, digest)
    sh.logger.info(f"###############本次执行结束###############\n\n")

