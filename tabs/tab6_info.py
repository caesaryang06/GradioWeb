import gradio as gr
import pandas as pd
import re
import os
import random
import sqlite3
from tools import customer_common_funcs as ccf



# 获取邮箱
def get_emails():

    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    emailsDF = pd.read_sql(
        'SELECT email_address,email_password FROM emails', conn)

    return emailsDF


# 获取软件账号
def get_accounts():

    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    accountsDF = pd.read_sql(
        'SELECT uuid,software_name,account,password,is_available FROM software_accounts', conn)

    return accountsDF


def get_choice():
    # 获取所有在使用的软件
    df = get_accounts()
    return df['software_name'].unique().tolist()


def get_email(software_name):
    """
    获取可用邮箱
    """
    df_software = get_accounts()
    df_email = get_emails()

    valid_email = ""
    valid_email_password = ""
    # 先看 software.xlsx 里面是否有对应的软件名称
    if software_name in df_software['software_name'].tolist():

        # 如果有状态为enable的邮箱，就返回第一个 并且根据这个邮箱地址从 df_email 中获取对应的邮箱的密码 返回邮箱和密码
        emails = df_software[(df_software['software_name'] == software_name) & (
            df_software['is_available'] == '可用')]['account'].tolist()
        if emails:
            valid_email = emails[0]
        else:
            # 列出所有不可用的邮箱
            disable_email_list = df_software[df_software['is_available']
                                             == '不可用']['account'].tolist()

            # 从 email.xlsx 中读取所有邮箱并过滤掉不可用的邮箱
            enable_email_list = df_email[~df_email['email_address'].isin(
                disable_email_list)]['email_address'].tolist()

            # 过滤 enable_email_list 中的 邮箱地址包含 "@163.com" 的邮箱
            enable_email_list = [
                email for email in enable_email_list if '@163.com' not in email]    
            
            valid_email = random.choice(enable_email_list)

    else:
        # 从 email.xlsx 中读取第一个邮箱地址不包含字符串 "@163.com" 的邮箱
        valid_email = df_email[~df_email['email_address'].str.contains(
            '@163.com')]['email_address'].tolist()[0]

    
    # 根据可用邮箱 valid_email  从 email.xlsx 中获取邮箱对应的密码
    # 根据可用邮箱 valid_email 先判断 email.xlsx 中是否包含可用邮箱 如果包含 则获取对应的密码并赋值
    if valid_email in df_email['email_address'].tolist():
        valid_email_password = df_email[df_email['email_address']
                                        == valid_email]['email_password'].tolist()[0]
        

    
    return valid_email, valid_email_password


# 新增软件使用情况
def add_software(software_name, account, password, enable):
    df = get_accounts()

       # 这里需要判断  如果 df 存在 软件名称 和 邮箱名称 相同的记录 则更新对应的记录 如果不存在 则添加
    if (df[(df['software_name'] == software_name) & (df['account'] == account)].empty):
        df.loc[len(df.index)] = [ccf.get_unique_value(software_name + account), software_name, account, password, enable]
    else:
        df.loc[(df['software_name'] == software_name) & (
            df['account'] == account), 'is_available'] = enable

    #  按照 软件名称 和 邮箱名称 去重
    df.drop_duplicates(subset=['software_name', 'account'],
                       keep='first', inplace=True)

    # 保存数据
    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    df.to_sql('software_accounts', conn, if_exists='replace', index=False)



def update_input(selected_option):
    # 根据选择的下拉选项更新输入框内容
    valid_email, valid_email_password = get_email(selected_option)
    
    return gr.Textbox(value=valid_email, interactive=True), valid_email_password


def refresh_result():
    return gr.Dropdown(choices=get_choice(), interactive=True)


def submit_result(software_name, account, password, enable):
    """
    根据模版对文本进行处理
    输入: 模版内容,输入文本
    输出: 基于模版内容处理后的文本
    样例: 模版内容: 我要{}成为{}的存在; 输入文本为: 小白@@@@伟人; 输出: 我要小白成为伟人的存在  
    """
    add_software(software_name, account, password, enable)
    df_software = get_accounts()


    # 当前软件账号信息
    dataDF = df_software[df_software['software_name']
                         == software_name] 
    resultDF = dataDF[['software_name', 'account', 'password', 'is_available']].rename(columns={'software_name': '软件名称','account': '账号', 'password': '密码', 'is_available': '是否可用'})
    
    # 所有软件账号信息
    allDF = df_software[['software_name', 'account', 'password', 'is_available']].rename(
        columns={'software_name': '软件名称', 'account': '账号', 'password': '密码', 'is_available': '是否可用'})

    
    
    return "操作成功",resultDF,ccf.export_to_excel(resultDF), ccf.export_to_excel(allDF)



def func():
    with gr.Row():
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=3):
                    dropdown = gr.Dropdown(
                        label="选择一个软件名称", choices=get_choice(), interactive=True, allow_custom_value=True)
                with gr.Column(scale=1):
                    refresh_btn = gr.Button(
                        value="刷新", icon="icon/refresh.icon")
            input_text = gr.Textbox(label="可用邮箱", interactive=False)
            input_passwd = gr.Textbox(label="邮箱密码", interactive=False)
            enable_radio = gr.Radio(["可用", "不可用"],
                                label="是否可用", info="请选择是否可用:", value="可用")
            with gr.Row():
                submit_btn = gr.Button("提交", variant="primary")                  
        with gr.Column():
            output_text = gr.Textbox(label="输出框")
            output = gr.Dataframe(label="Table",headers=["软件名称","账号","密码","是否可用"])
            download_file = gr.File(label="当前结果下载")
            all_download_file = gr.File(label="所有账号下载")

    # 设置下拉选项修改事件
    dropdown.change(fn=update_input, inputs=dropdown,
                    outputs=[input_text,input_passwd])
    
    # 刷新按钮点击事件
    refresh_btn.click(fn=refresh_result, inputs=[],outputs=[dropdown])


    # 设置提交点击事件
    submit_btn.click(fn=submit_result,
                     inputs=[dropdown, input_text, input_passwd, enable_radio], outputs=[output_text, output, download_file, all_download_file],)
