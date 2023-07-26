from langchain.chat_models import ChatOpenAI
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
    template_string = """
    Translate the text that is delimited by triple backticks into a style that is {style}.\
    text: '''{text}'''
    """
    prompt_template = ChatPromptTemplate.from_template(template=template_string)
    print(prompt_template.messages[0].prompt.input_variables)
    customer_style = """
    American English in a calm and respectful tone
    """
    customer_email = """
    Arrr, i be fuming that me blender lid \
    flew off and splattered me kitchen walls \
    with smoothie! And to make matters worse, \
    the warranty don't cover the cost of \
    cleaning up me kitchen. I need yer help \
    reight now, matey!                                                                                   
    """
    customer_messages = prompt_template.format_messages(
        style=customer_style,
        text=customer_email
    )
    print(type(customer_messages))
    print(type(customer_messages[0]))
    print(customer_messages)
    customer_response = chat(customer_messages)
    print(customer_response.content)
