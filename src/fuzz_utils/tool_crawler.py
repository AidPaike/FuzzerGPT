from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

from src.ality_functions.func_crawler import WebScraper
# 在conf中设置了代理和密钥
from conf import fuzzgpt_globals


@tool
def get_bugreport(bug_id: str) -> str:
    """Send a get request to the given bug_id \
    Returns url bug_id data for any issues related to link to \
    https://bugs.java.com/bugdatabase/view_bug?bug_id= \
    at the beginning. The input should always be the id number after bug_id= \
    This function will always return () function returns the data ."""
    scraper = WebScraper('https://bugs.java.com/bugdatabase/view_bug?bug_id=')
    try:
        data = scraper.scrape(bug_id=bug_id)
    except Exception as e:
        data = e
        print('Error:', e)
    return data


if __name__ == '__main__':
    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent(
        [get_bugreport],
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=False)
    try:
        result = agent("please get https://bugs.java.com/bugdatabase/view_bug?bug_id=8212070 content")
        print(result)
    except:
        print("exception on external access")
