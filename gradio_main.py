import gradio as gr
from tabs import tab1_info, tab2_info, tab3_info, tab4_info, tab5_info, tab6_info,tab7_info, tab8_info,tab9_info
import sys
from tools.common_log import setup_logger
from tools import customer_common_funcs as ccf

# 加载 .env 文件
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# 设置日志
log_file = ccf.getCurrentDateStr() + ".log"
logger = setup_logger(log_file)




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
            with gr.Tab("批量视频识别"):
                tab4_info.func()
            with gr.Tab("邮箱管理"):
                tab5_info.func()      
            with gr.Tab("软件账号管理"):
                tab6_info.func()
            with gr.Tab("音频/视频分割"):
                tab7_info.func()
            with gr.Tab("长短链接转换"):
                tab8_info.func()
            with gr.Tab("提示词管理"):
                tab9_info.func()               

    if sys.platform.startswith('win'):
        app.launch(inbrowser=True, auth=login, share=False)
    else:
        app.launch(inbrowser=True, auth=login, share=True)
