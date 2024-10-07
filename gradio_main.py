import gradio as gr
from tabs import tab1_info, tab2_info, tab3_info, tab4_info
import sys

# 加载 .env 文件
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# 登录验证函数
def login(username, password):
    return username == "admin" and password == "admin"



if __name__ == "__main__":
   
    

    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.Tab("生成随机密码"):
                tab1_info.func()
            with gr.Tab("密码加解密"):
                tab2_info.func()
            with gr.Tab("单个语音识别"):
                tab3_info.func()
            with gr.Tab("批量语音识别"):
                tab4_info.func()

    if sys.platform.startswith('win'):
        app.launch(inbrowser=True, auth=login, share=False)
    else:
        app.launch(inbrowser=True, auth=login, share=True)
