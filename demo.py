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


with gr.Blocks() as demo:
    gr.Markdown("# 长短链接转换")

    with gr.Tab("链接转换"):
        with gr.Row():
            long_input = gr.Textbox(label="长链接")
            short_input = gr.Textbox(label="短链接")

        with gr.Row():
            long_to_short_btn = gr.Button("长链接 → 短链接")
            short_to_long_btn = gr.Button("短链接 → 长链接")

        # 使用 show_copy_button 选项
        result_output = gr.Textbox(
            label="转换结果",
            interactive=False,
            show_copy_button=True
        )

        long_to_short_btn.click(
            long_to_short,
            inputs=[long_input],
            outputs=[result_output]
        )

        short_to_long_btn.click(
            short_to_long,
            inputs=[short_input],
            outputs=[result_output]
        )

demo.launch()
