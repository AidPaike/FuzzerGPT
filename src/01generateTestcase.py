import openai
import os, requests, json
from bs4 import BeautifulSoup

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

# 在conf中设置了代理和密钥
from conf import fuzzgpt_globals

chat = ChatOpenAI(temperature=0)


def is_target_tag(tag):
    target_tags = ['p', 'code', 'h1', 'h2', 'h2', 'h3', 'h4', 'h5']
    return tag.name in target_tags


def get_text_from_url(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    extracted_tags = soup.find_all(is_target_tag)
    res_text = ''
    for tag in extracted_tags:
        res_text = res_text + tag.get_text(strip=True) + '\n'
    return res_text


functions = [
    {
        "name": "get_text_from_url",
        "description": "抓取url对应的网页里的文本内容",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "网址url",
                }
            },
            "required": ["url"],
        },
    }
]

available_functions = {
    "get_text_from_url": get_text_from_url,
}


def chat(content):
    messages = [
        {"role": "user", "content": content}
    ]
    response1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response1["choices"][0]["message"]
    rtn_message = response1["choices"][0]["message"]
    # 如果ChatGPT返回结果会告诉你，是否需要调用函数，我们只需要根据它返回的函数名、参数调起对应的函数
    # 然后将函数的返回结果再给到ChatGPT，让他进行下一步的操作
    if response_message.get("function_call"):
        # 找到需要调用的函数，并将ChatGPT给的参数传进去
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        # 用这种方式可以调起任意python函数，不用像官网那样还要指定参数名
        function_response = fuction_to_call(**function_args)
        # 获取到函数调用结果后，需要将结果拼接到对话记录里，并再次调用ChatGPT
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        # 二次调用的返回结果里就是我们预期的结果了
        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )
        rtn_message = response2["choices"][0]["message"]
    return rtn_message['content']




if __name__ == '__main__':
    chat('总结下这篇文章，将其中的要点提炼出来 https://zxs.io/article/1924')

