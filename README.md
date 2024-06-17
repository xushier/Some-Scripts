## 获取磁力并提交到 115 离线，清理垃圾。

## 第一次使用建议操作
1. 青龙添加任务。名称和定时随意。命令填写：`ql repo https://mirror.ghproxy.com/https://github.com/xushier/Some-Scripts.git "xd" "" "__"`。添加后执行一次。
2. 导入环境变量。可以参照下面的使用说明一个个添加，**也可以下载 sht 文件夹的 json 文件，在青龙面板环境变量菜单导入，[json 文件](https://github.com/xushier/Some-Scripts/blob/main/sht/import_vars.json)**
3. 参照下面的使用说明修改环境变量值。
4. 在青龙面板依赖管理菜单安装 python3 依赖：requests、pymongo、clouddrive、grpcio。

## 使用说明
需搭配 **青龙面板、CloudDrive** 使用。
1. - 打开青龙面板，添加以下任务。
   - 名称随便输入；
   - 定时规则随便输入，若不知道怎么输入，输入0 0 * * *即可；
   - 命令/脚本输入：`ql repo https://mirror.ghproxy.com/https://github.com/xushier/Some-Scripts.git "xd" "" "__"`
2. 添加后点击右侧按钮运行一次。添加后界面会多出来两个名称分别为 xdSht 和 xdShtClean 的任务。xdSht 是添加并局部清理脚本，每天运行一次即可，建议晚上十点以后运行。xdShtClean 是清理脚本，根据需要可定时全量或局部清理。两个脚本可独立运行。
3. 进入青龙面板的依赖管理界面，选择 Python3 ，名称输入 pymongo ，确定后等待依赖安装完成。按照以上操作再安装 requests、clouddrive、grpcio。理论上即使不装脚本也会自动安装。
4. 进入青龙面板的环境变量界面，点击创建变量，依次添加如下变量。也可使用代码同文件夹下的 import_vars.json 文件快速导入变量，注意不要重名了。

| 变量名      | 作用                   | 说明                                                         |
| :---------- | :--------------------- | :----------------------------------------------------------- |
| cd2_url     | cd2 地址               | 必填。需填写 http 前缀。                                     |
| cd2_usr     | cd2 用户名             | 必填                                                         |
| cd2_pwd     | cd2 密码               | 必填                                                         |
| save_path   | cd2 内的保存路径       | 必填。路径以 /115 开头。                                     |
| mount_path  | 主机的挂载路径         | 必填。为主机挂载路径对应的容器内路径。<br />路径填写至 SHT 上一级即可。如 /mnt/115/SHT，则填 /mnt/115 |
| add_mode    | 添加模式               | 可选值 1/2，不加默认为 1，即添加后清理局部（三日内）垃圾。<br />2 为仅添加不清理。 |
| clean_mode  | 清理模式               | 可选值 1/2，不加默认不清理。<br />若为 1 ，则开启全量清理；若为 2，则开启清理局部垃圾。 |
| XD_QYWX_APP | 企业微信通知相关信息。 | 值同青龙面板的 QYWX_AM 变量。**五个参数，英文逗号隔开，最后一个为 media_id。** |
| account_id | 需要显示配额的 115 账户昵称 | 可在 115 手机客户端个人信息页面查看。 |

6. 任务命令 `task xushier_Some-Scripts/sht/sht.py` 后可传入两个参数。 
   - 第一个为日期。单日：2024-01-01     多日：2024-01-01,2024-01-05    默认：昨日
   - 第二个为分类。单类：动漫           多类：动漫-4K-VR                默认：所有
   - 例：`task xushier_Some-Scripts/sht/sht.py 2024-01-01,2024-01-05 动漫-4K-VR`
7. 需要企业微信通知需要添加变量 XD_QYWX_APP，格式参考青龙面板：`corpid,corpsecret,touser(注:多个成员ID使用|隔开),agentid,消息类型(选填,不填默认文本消息类型) 注意用,号隔开(英文输入法的逗号)，例如：wwcfrs,B-76WERQ,qinglong,1000001,2COat`
8. 需要企业微信可信代理需要添加变量 XD_QYWX_PROXY
9. 若需要自定义保存分类文件夹名。可添加以下变量。变量值为自己需要的文件夹名。
```
uhd_video
anime_originate
asia_codeless_originate
asia_mosaic_originate
domestic_original
EU_US_no_mosaic
hd_chinese_subtitles
vegan_with_mosaic
vr_video
three_levels_photo
```
9. 其他通知渠道参考以下：
```BARK_PUSH         # bark IP 或设备码，例：https://api.day.app/DxHcxxxxxRxxxxxxcm/
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

XD_QYWX_APP       # 企业微信应用

QYWX_KEY          # 企业微信机器人
XD_QYWX_PROXY     # 企业微信可信代理

TG_BOT_TOKEN      # tg 机器人的 TG_BOT_TOKEN，例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
TG_USER_ID        # tg 机器人的 TG_USER_ID，例：1434078534
TG_API_HOST       # tg 代理 api
TG_PROXY_AUTH     # tg 代理认证参数
TG_PROXY_HOST     # tg 机器人的 TG_PROXY_HOST
TG_PROXY_PORT     # tg 机器人的 TG_PROXY_PORT
```
