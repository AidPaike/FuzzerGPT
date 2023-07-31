from langchain.prompts import ChatPromptTemplate


def get_generate_template():
    generate_prompt = ChatPromptTemplate.from_template(
        """summarize {bug_report_content} how the bug was triggered and\
            based on your experience, generate a piece of \
           java test cases that can be executed and reproduce the bug error \ 
            just show the tese case code use string in the final answer\
            output Use the following format: \
            description: the final description to the original input question,\
            code: the final code to the original input question
        """

    )

    return generate_prompt
