## 获取磁力并提交到 115 离线。

## 使用说明
需搭配 **青龙面板、CloudDrive** 使用。
1. - 打开青龙面板，添加以下任务。
   - 名称随便输入；
   - 定时规则随便输入，若不知道怎么输入，输入0 0 * * *即可；
   - 命令/脚本输入：`ql repo https://github.com/xushier/Some-Scripts.git "Sht" "" "__notifier"`
2. 添加后点击右侧按钮运行一次。添加后界面会多出来一个名称为 Sht.py 的任务。
3. 进入青龙面板的依赖管理界面，选择 Python3 ，名称输入 pymongo ，确定后等待依赖安装完成。按照以上操作再安装 requests、clouddrive
4. 进入青龙面板的环境变量界面，点击创建变量，依次添加名称为 cd2_url、cd2_usr、cd2_pwd、save_path、mount_path、clean_all 的环境变量，值分别为 Clouddrive 的访问地址、用户名、密码、在 Clouddrive 里看到的要保存到的路径、save_path 对应挂载到本地的路径，以及清理垃圾是否清理所有，默认为 False。
5. 任务命令 `task xushier_Some-Scripts/Sht.py` 后可传入三个参数。 
   - 第一个为日期。单日：2024-01-01     多日：2024-01-01,2024-01-05    默认：昨日
   - 第二个为分类。单类：动漫           多类：动漫-4K-VR                默认：所有
   - 第三个为清理。默认为 False，关闭清理。开启为 True
   - 例：`task xushier_Some-Scripts/Sht.py 2024-01-01,2024-01-05 动漫-4K-VR True`
6. 需要企业微信通知需要添加变量 QYWX，格式参考青龙面板：`corpid,corpsecret,touser(注:多个成员ID使用|隔开),agentid,消息类型(选填,不填默认文本消息类型) 注意用,号隔开(英文输入法的逗号)，例如：wwcfrs,B-76WERQ,qinglong,1000001,2COat`
7. 需要企业微信可信代理需要添加变量 QYWX_PROXY
8. 若需要自定义保存分类文件夹名。可添加以下变量：
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

QYWX_AM           # 企业微信应用
QYWX_KEY          # 企业微信机器人
QYWX_PROXY        # 企业微信可信代理

TG_BOT_TOKEN      # tg 机器人的 TG_BOT_TOKEN，例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
TG_USER_ID        # tg 机器人的 TG_USER_ID，例：1434078534
TG_API_HOST       # tg 代理 api
TG_PROXY_AUTH     # tg 代理认证参数
TG_PROXY_HOST     # tg 机器人的 TG_PROXY_HOST
TG_PROXY_PORT     # tg 机器人的 TG_PROXY_PORT
```
