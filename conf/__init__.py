import openai
import os
from conf import fuzzgpt_constants
import re

constants_conf = fuzzgpt_constants.Constants()

__version__ = '1.0.0'


# 判断是否符合密钥格式
def is_valid_openai_key(api_key):
    # 定义OpenAI密钥的格式正则表达式
    pattern = r'^sk-[a-zA-Z0-9]{48}$'
    return bool(re.match(pattern, api_key))


# 设置代理
openai.proxy = "http://127.0.0.1:7890"
# 设置oepnai的密钥
openai_api_key = os.getenv("OPENAI_APIKEY")

# print("成功设置代理和密钥")
# 如果没有找到密钥，终止程序并报错
if not openai_api_key:
    if is_valid_openai_key(constants_conf.OPENAI_API_KEY):
        openai_api_key = constants_conf.OPENAI_API_KEY
    else:
        raise ValueError(
            "OpenAI API key not found in environment variables. Please set the OPENAI_API_KEY environment variable in conf/constants or enviroment.")
