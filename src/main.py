from langchain.chat_models import ChatOpenAI
# 在conf中设置了代理和密钥
from conf import fuzzgpt_globals

chat = ChatOpenAI()

print(chat)