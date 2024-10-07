import gradio as gr
import os
from tools import customer_common_funcs as ccf
from pydub import AudioSegment
import zipfile


# 将多个文件压缩成一个zip文件
def zip_all_files(files, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file)


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

# 批量处理视频转音频
def movie2voice(audio_files):
    # 指定临时目录
    temp_dir = "out/m2v/tmp"

    # 清空临时目录下的文件
    ccf.delete_folder_contents(temp_dir)

    result = []

    # 使用Whisper进行语音识别
    for audio_file in audio_files:
        print(f"【视频转音频】开始处理：{audio_file}")
        mvfile = os.path.basename(audio_file)
        output_mp3_path = temp_dir + "/" + mvfile.replace("mp4", "mp3")
        audio = AudioSegment.from_file(audio_file, format='mp4')
        audio.export(output_mp3_path, format="mp3")
        result.append(output_mp3_path)
        print(f"【视频转音频】处理完成：{audio_file}")

    return result


def submit_result(op, audio_files):

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
        with gr.Column():
            input_files = gr.Files(label="文件", type='filepath',
                                    file_count="directory", visible=True)
            op_radio = gr.Radio(["字幕文件生成", "音频文件生成"],
                                label="操作类型", info="请选择操作类型:", value="字幕文件生成")
            submit_btn = gr.Button("开始处理",variant="primary")
        with gr.Column():
            output_audio = gr.File(label="输出文件明细")
            zip_audio = gr.File(label="输出压缩文件")

    # 设置提交点击事件
    submit_btn.click(fn=submit_result,
                     inputs=[op_radio, input_files], outputs=[output_audio,zip_audio])
