import asyncio, time
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.prompts import ChatPromptTemplate
from src.fuzz_utils.tool_crawler import get_bugreport
from src.fuzz_utils.tool_prompt import get_generate_template
from utils.db_connect import MongoDBHandle

# 在conf中设置了代理和密钥
from conf import fuzzgpt_globals

'''
import 推荐方法
第一部分：standard library
第二部分：third party library
第三部分：local


先写import 再写 from import
尽可能避免import *
'''

if __name__ == '__main__':
    # 初始化数据库
    mongodb_connection = MongoDBHandle()

    # 定义llm
    llm = ChatOpenAI(temperature=0)

    # 定义ids
    ids = ["8212070", "8212070"]

    generate_chain = LLMChain(llm=llm, prompt=get_generate_template())

    generate_tool = Tool(
        name='Generate java test cases code Model',
        func=generate_chain.run,
        description='Use this tool to generate java test cases that trigger bug reports'
    )

    agent = initialize_agent(
        [generate_tool, get_bugreport],
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True)
    try:
        # s = time.perf_counter()
        # tasks = [agent.arun(q) for q in ids]
        # await asyncio.gather(*tasks)
        # elapsed = time.perf_counter() - s
        # print(f"Concurrent executed in {elapsed:0.2f} seconds.")
        result = agent(
            "please get https://bugs.java.com/bugdatabase/view_bug?bug_id=8212070 content and generate test case based on this report"
        )
        print(result)
        print(type(result))
        one_return = mongodb_connection.insert_code_one(result)
        mongodb_connection.close()
        print("已存入数据库，请查看")
    except:
        print("exception on external access")
