import gradio as gr
import pandas as pd
import sqlite3
import tempfile


# 初始化数据框
# 连接到SQLite数据库
conn = sqlite3.connect('data.db')
# 读取表数据到DataFrame
df = pd.read_sql('SELECT * FROM emails', conn)


def add_row(address_input, password_input, search_input):
    global df
    new_row = pd.DataFrame(
        {'email_address': [address_input], 'email_password': [password_input]})
    df = pd.concat([df, new_row], ignore_index=True)

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df


def delete_row(address_input, password_input, search_input):
    global df
    df = df[df['email_address'] != address_input]

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df


def update_row(address_input, password_input, search_input):
    global df
    df.loc[df['email_address'] == address_input,
           ['email_password']] = [password_input]

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df


def search(address_input, password_input, search_input):
    return df[df['email_address'].str.contains(search_input, case=False)]


def show_table(address_input, password_input, search_input):
    return df


def export_to_excel(df):
    # 创建一个临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False)
        tmp_path = tmp.name
    return tmp_path



    # 定义函数字典
    dict_operations = {
        "字幕文件生成": transcribe_audios,
        "音频文件生成": movie2voice,
    }
    list_files = dict_operations[op](audio_files)

    # 将结果列表中的所有文件压缩成一个zip文件
    basedir = "out/sr2/tmp/" if op == "字幕文件生成" else "out/m2v/tmp/"
    zip_name = basedir + ccf.getCurrentDateStr() + ".zip"
    zip_all_files(list_files, zip_name)

    return list_files,[zip_name]

def func():
    with gr.Row():
        address_input = gr.Textbox(label="邮箱地址")
        password_input = gr.Textbox(label="邮箱密码")
        search_input = gr.Textbox(label="邮箱地址模糊搜索")

    with gr.Row():
        add_button = gr.Button("新增记录", variant="primary")
        del_button = gr.Button("删除记录", variant="primary")
        update_button = gr.Button("修改记录", variant="primary")
        search_button = gr.Button("搜索记录", variant="primary")
        all_button = gr.Button("全部记录", variant="primary")

    output = gr.Dataframe(label="Table")

    add_button.click(
        add_row,
        inputs=[address_input, password_input, search_input],
        outputs=output
    )

    del_button.click(
        delete_row,
        inputs=[address_input, password_input, search_input],
        outputs=output
    )

    update_button.click(
        update_row,
        inputs=[address_input, password_input, search_input],
        outputs=output
    )

    search_button.click(
        search,
        inputs=[address_input, password_input, search_input],
        outputs=output
    )

    all_button.click(
        show_table,
        inputs=[address_input, password_input, search_input],
        outputs=output
    )
