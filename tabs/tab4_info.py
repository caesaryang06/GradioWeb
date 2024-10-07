import whisper
import gradio as gr
import os
from tools import customer_common_funcs as ccf



# 批量处理语音识别
def transcribe_audios(audio_files):

    # 指定临时目录
    temp_dir = "out/sr2/tmp"

    # 清空临时目录下的文件
    ccf.delete_folder_contents(temp_dir)

    # 使用Whisper进行语音识别
    for audio_file in audio_files:
        os.system('whisper "{}" --model medium --output_format all --output_dir {}'.format(audio_file, temp_dir))


    #获取结果列表
    result = [ temp_dir + "/" + file for file in ccf.list_files_in_directory(temp_dir)]

    return result


def func():
    with gr.Row():
        with gr.Column():
            input_files = gr.Files(label="文件", type='filepath',
                                    file_count="directory", visible=True)
            submit_btn = gr.Button("开始识别",variant="primary")
        with gr.Column():
            output_audio = gr.File(label="输出")

    # 设置提交点击事件
    submit_btn.click(fn=transcribe_audios,
                     inputs=input_files, outputs=output_audio)
