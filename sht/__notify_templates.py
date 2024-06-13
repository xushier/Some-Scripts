#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from __initial_vars import *

def add_content(cd2, add, date):
    total_add, total_clean = 0, 0
    for value in add.values():
        total_add += value[1]
        if and_clean and isinstance(value[2], int):
            total_clean += value[2]
    add_content=f"""
    <table style="border-radius: 25px;overflow: hidden;font-size: 14px;font-weight: 500;font-family: -apple-system-font, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial;border-collapse: collapse;width: 100%;letter-spacing: 1px;text-align: center;">
        <tr style="border: 1px solid #a35c8f;background-color: #8A3782;color: white;font-size: 18px;">
            <th colspan="3" style="padding: 8px;"><p>大姐姐探测仪</p><p style="font-size: 12px">{date}</p></td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #681752;color: white;font-size: 16px;">
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">CD2</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">已用</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">可用</th>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{cd2['mount']}</td>
            <td style="padding: 8px;">{cd2['used']}</td>
            <td style="padding: 8px;">{cd2['free']}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;font-size: 13px;">
            <td colspan="3" style="padding: 8px;">当前版本：{cd2['nowVersion']} {cd2['hasUpdate']} {cd2['newVersion']}<br>{cd2['updateLog']}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #681752;color: white;font-size: 16px;">
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">分类</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">添加</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">清理</th>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{add['asia_codeless_originate'][0]}</td>
            <td style="padding: 8px;">{add['asia_codeless_originate'][1]}</td>
            <td style="padding: 8px;">{add['asia_codeless_originate'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;">
            <td style="padding: 8px;">{add['asia_mosaic_originate'][0]}</td>
            <td style="padding: 8px;">{add['asia_mosaic_originate'][1]}</td>
            <td style="padding: 8px;">{add['asia_mosaic_originate'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{add['EU_US_no_mosaic'][0]}</td>
            <td style="padding: 8px;">{add['EU_US_no_mosaic'][1]}</td>
            <td style="padding: 8px;">{add['EU_US_no_mosaic'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;">
            <td style="padding: 8px;">{add['vegan_with_mosaic'][0]}</td>
            <td style="padding: 8px;">{add['vegan_with_mosaic'][1]}</td>
            <td style="padding: 8px;">{add['vegan_with_mosaic'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{add['hd_chinese_subtitles'][0]}</td>
            <td style="padding: 8px;">{add['hd_chinese_subtitles'][1]}</td>
            <td style="padding: 8px;">{add['hd_chinese_subtitles'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;">
            <td style="padding: 8px;">{add['domestic_original'][0]}</td>
            <td style="padding: 8px;">{add['domestic_original'][1]}</td>
            <td style="padding: 8px;">{add['domestic_original'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{add['anime_originate'][0]}</td>
            <td style="padding: 8px;">{add['anime_originate'][1]}</td>
            <td style="padding: 8px;">{add['anime_originate'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;">
            <td style="padding: 8px;">{add['three_levels_photo'][0]}</td>
            <td style="padding: 8px;">{add['three_levels_photo'][1]}</td>
            <td style="padding: 8px;">{add['three_levels_photo'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #894276;color: white;">
            <td style="padding: 8px;">{add['4k_video'][0]}</td>
            <td style="padding: 8px;">{add['4k_video'][1]}</td>
            <td style="padding: 8px;">{add['4k_video'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #7e2065;color: white;">
            <td style="padding: 8px;">{add['vr_video'][0]}</td>
            <td style="padding: 8px;">{add['vr_video'][1]}</td>
            <td style="padding: 8px;">{add['vr_video'][2]}</td>
        </tr>
        <tr style="border: 1px solid #a35c8f;background-color: #681752;color: white;font-size: 16px;">
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">合计</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">{total_add}</th>
            <th style="padding: 8px;padding-top: 12px;padding-bottom: 12px;">{total_clean}</th>
        </tr>
    """

    return add_content, total_add, total_clean

