import os
import shutil
from pypinyin import pinyin, Style
  
def to_pinyin(chinese_text, style=Style.NORMAL):
    """
    将汉字转换为拼音
    :param chinese_text: 汉字文本
    :param style: 拼音风格，例如 Style.NORMAL, Style.TONE, Style.TONE2, Style.TONE3, Style.INITIALS, Style.FINALS
    :return: 拼音列表
    """
    return ' '.join([''.join(p for p_list in pinyin(char, style=style) for p in p_list) for char in chinese_text])


source_path = "/mnt/cacheqb/Download/test"
dest_path   = "/mnt/cacheqb/Download/test1"

def move(source_path, dest_path):
    # 移动源目录下文件或文件夹到首字母目标目录下
    for sub_name in os.listdir(source_path):
        sub_path     = os.path.join(source_path, sub_name)
        first_letter = to_pinyin(sub_name, style=Style.INITIALS)[0].upper()
        letter_path  = os.path.join(dest_path, first_letter)

        if not os.path.exists(letter_path):
            os.makedirs(letter_path)
        shutil.move(sub_path, letter_path)
        print(f"移动 {sub_name} 到 {letter_path}")

move(source_path, dest_path)

