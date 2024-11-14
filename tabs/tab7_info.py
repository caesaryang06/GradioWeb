import gradio as gr
from moviepy.editor import *
import os
import tempfile
import math
from tools import customer_common_funcs as ccf


def split_media(file, segment_length, output_format):
    # 获取原文件名（不包括扩展名）
    base_name = os.path.splitext(os.path.basename(file))[0]

    # 加载媒体文件
    if file.endswith(('.mp4', '.avi', '.mov')):
        clip = VideoFileClip(file)
    else:
        clip = AudioFileClip(file)

    # 计算需要分割的段数
    total_duration = clip.duration
    num_segments = math.ceil(total_duration / segment_length)

    output_files = []
    for i in range(num_segments):
        start = i * segment_length
        end = min((i + 1) * segment_length, total_duration)

        subclip = clip.subclip(start, end)

        # 使用格式化的文件名
        output_filename = f"out/media/tmp/{base_name}{i+1:03d}.{output_format}"

        if isinstance(clip, VideoFileClip):
            subclip.write_videofile(output_filename, codec='libx264')
        else:
            subclip.write_audiofile(output_filename)

        output_files.append(output_filename)

    clip.close()
    return output_files


def merge_media(files, output_format):
    # 合并功能保持不变
    clips = []
    for file in files:
        if file.name.endswith(('.mp4', '.avi', '.mov')):
            clips.append(VideoFileClip(file.name))
        else:
            clips.append(AudioFileClip(file.name))

    merged_clip = concatenate_videoclips(clips) if isinstance(
        clips[0], VideoFileClip) else concatenate_audioclips(clips)

    output_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=f'.{output_format}')
    if isinstance(merged_clip, VideoFileClip):
        merged_clip.write_videofile(output_file.name, codec='libx264')
    else:
        merged_clip.write_audiofile(output_file.name)

    for clip in clips:
        clip.close()
    merged_clip.close()

    return [output_file.name]


def process_media(operation, input_files, segment_length, output_format):

    # 清空临时文件
    ccf.delete_folder_contents("out/media/tmp")

    if operation == "Split":
        listFiles = split_media(input_files, segment_length, output_format)

    elif operation == "Merge":
        listFiles = merge_media(input_files, output_format)

    # 将结果列表中的所有文件压缩成一个zip文件
    basedir = "out/media/tmp/"
    zip_name = basedir + ccf.getCurrentDateStr() + ".zip"
    ccf.zip_all_files(listFiles, zip_name)

    return listFiles, zip_name



def func():
    with gr.Row():
        operation = gr.Radio(["Split", "Merge"], label="操作类型")

    with gr.Row():
        input_files = gr.File(label="输入文件", file_count="multiple")
        segment_length = gr.Number(label="分割长度（秒）", value=60, visible=False)
        output_format = gr.Dropdown(choices=["mp3", "mp4", "wav"], label="输出格式")

    submit_button = gr.Button("执行", variant="primary")

    output = gr.File(label="输出文件明细", file_count="multiple")
    zip_output = gr.File(label="输出压缩文件")

    def update_visibility(operation):
        if operation == "Split":
            return gr.update(file_count="single"), gr.update(visible=True)
        else:
            return gr.update(file_count="multiple"), gr.update(visible=False)

    operation.change(
        update_visibility,
        inputs=[operation],
        outputs=[input_files, segment_length]
    )

    submit_button.click(
        process_media,
        inputs=[operation, input_files, segment_length, output_format],
        outputs=[output, zip_output]
    )
