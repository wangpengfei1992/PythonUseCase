#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/02/08 14:42:26
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : ChatGPT 简易测试
'''

# 安装open AI pip3 install openai

import os
import openai

start_sequence = "\nA:"
restart_sequence = "Q: "

# Replace `<your_api_key>` with your actual OpenAI API key
openai.api_key = "-----"
prompt = " "

while len(prompt)!=0:
    # Ask a question
    prompt = input(restart_sequence)
    #prompt = "tell me in Chinese:" + input("\n请输入要翻译的内容：")
 
    # Get my answer
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0
    )
 
    # Print my answer
    print(start_sequence,response["choices"][0]["text"].strip())
