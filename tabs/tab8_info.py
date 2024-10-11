import gradio as gr
import pyshorteners
import pyperclip


# 初始化 URL 缩短器
shortener = pyshorteners.Shortener()


def long_to_short(long_url):
    try:
        short_url = shortener.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return f"发生错误: {str(e)}"


def short_to_long(short_url):
    try:
        long_url = shortener.tinyurl.expand(short_url)
        return long_url
    except Exception as e:
        return f"发生错误: {str(e)}"


def submit_result(op_radio, input_link):
    if op_radio == "长链接 → 短链接":
        return long_to_short(input_link)
    elif op_radio == "短链接 → 长链接":
        return short_to_long(input_link)



def copy_result(text):
    pyperclip.copy(text)
    print("已复制到剪贴板")
    


def func():
    op_radio = gr.Radio(["长链接 → 短链接", "短链接 → 长链接"],
                            label="操作类型", value="长链接 → 短链接")
    input_link = gr.Textbox(label="请输入链接", show_copy_button=True,show_label=True)
    
    submit_btn = gr.Button("转换",variant="primary")

    result_output = gr.Textbox(
        label="转换结果", interactive=False, show_copy_button=True, show_label=True)
    copy_btn = gr.Button("复制结果", variant="secondary")

    submit_btn.click(
        submit_result,
        inputs=[op_radio, input_link],
        outputs=[result_output]
    )

    copy_btn.click(copy_result, inputs=[result_output], outputs=[])
