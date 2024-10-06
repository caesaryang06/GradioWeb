from pydub import AudioSegment
import shutil
import os
from moviepy.editor import VideoFileClip
import math
import os
import uuid
import time
import datetime


from pydub import AudioSegment


# 将 WAV 文件转换为 MP3 文件。
def convert_wav_to_mp3(audio_files, output_dir):
    """
    批量将wav文件处理成mp3文件
    """

    result = []
    for audio_file in audio_files:
        # 加载 WAV 文件
        audio = AudioSegment.from_wav(audio_file)
        # 导出为 MP3 文件
        basename = os.path.basename(audio_file)
        output_mp3_path = output_dir + "/" + basename.split(".")[0] + ".mp3"
        audio.export(output_mp3_path, format="mp3")
        print(f"Conversion complete: {output_mp3_path}")

        result.append(output_mp3_path)


    return result





# 返回指定路径下的所有文件名称
def list_files_in_directory(directory_path):
    """
    返回指定路径下的所有文件名称

    Args:
    directory_path (str): The path to the directory from which to list files.

    Returns:
    list: A list of file names in the directory.
    """
    file_names = []  # Initialize an empty list to store file names
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)  # Create full path
        if os.path.isfile(file_path):  # Check if it is a file
            file_names.append(filename)
    return file_names


# 获取当前日期，格式为"YYYYMMDD"
def getCurrentDateStr():
    """
    获取当前日期，格式为"YYYYMMDD"
    """
    today = datetime.date.today()
    return str(today).replace("-", "")


# 传入多个变量返回第一个不为None的值
def first_not_none(*args):
    """
    传入多个变量返回第一个不为None的值
    """
    for arg in args:
        if arg is not None:
            return arg
    return None


# 获取当前时间戳
def get_current_timestamp():
    return int(time.time())


# 获取uuid
def get_uuid():
    return str(uuid.uuid4())


# 获取指定路径下文件的个数
def count_files(directory_path):
    # 计数变量初始化
    file_count = 0

    # 遍历指定目录下的所有文件和文件夹
    for entry in os.listdir(directory_path):
        # 拼接完整的文件或文件夹路径
        full_path = os.path.join(directory_path, entry)

        # 检查这个路径是否是文件
        if os.path.isfile(full_path):
            file_count += 1

    return file_count


# 获取指定视频的帧数
def get_frame_count(video_path):
    '''
    获取指定视频的帧数
    '''
    # 加载视频文件
    video = VideoFileClip(video_path)

    # 获取视频的帧率（fps）和时长（duration）
    fps = video.fps
    duration = video.duration

    # 计算总帧数
    frame_count = int(fps * duration) + 1

    # 关闭视频文件
    video.close()

    return frame_count


# 计算文本中包含多少个{}
def count_brackets(text):
    """
    计算文本中包含多少个{}
    """
    return text.count('{}')


# 音频文件切分，将指定音频文件按照指定的时间长度切分成多个片段
def split_audio(audio_file, output_dir, split_length_seconds):
    """

     返回值： 存储片段路径的数组
     调用样例： split_audio("input.mp3", "output_dir", 10)  # 分割input.mp3，每个分割片段长度为10秒，保存到output_dir目录

    """
    # 加载音频文件
    audio = AudioSegment.from_file(audio_file, format="mp3")
    # AudioSegment.from_mp3(input_file)

    # 计算分割点
    split_points = list(range(0, len(audio), int(split_length_seconds * 1000)))

    # 用于存储返回音频片段的路径
    return_audio_paths = []

    # 分割音频并保存
    for i, split_point in enumerate(split_points):
        split_audio = audio[split_point:split_point +
                            int(split_length_seconds * 1000)]
        output_file = f"{output_dir}/split_audio_{i}.mp3"
        split_audio.export(output_file, format="mp3")

        # 音频文件路径添加到数组中
        return_audio_paths.append(output_file)
    
    return return_audio_paths


# 音频文件合并
def merge_audio(audio_files, output_dir):
    """
    合并音频文件
    输入参数说明：
      audio_files   [ "path/to/audio1.mp3",  "path/to/audio2.mp3" ]  
      output_file   "out"
    返回结果说明：  返回生成合并后的音频文件的路径
    """

    # 初始化一个空的AudioSegment对象
    merged_audio = AudioSegment.empty()

    # 循环遍历所有音频文件，并将它们添加到merged_audio中
    for audio_file in audio_files:
        audio_segment = AudioSegment.from_mp3(audio_file)
        merged_audio = merged_audio + audio_segment


    # 将合并后的音频保存为新文件
    out_file = f"{output_dir}/merged_audio.mp3"   
    merged_audio.export(out_file, format="mp3")
   
    return [out_file]


# 删除指定文件夹内的所有内容
def delete_folder_contents(folder_path):
    """
    删除指定文件夹下的所有内容
    """
        # 检查文件夹是否存在  
    if os.path.exists(folder_path):  
        # 删除文件夹及其所有内容  
        shutil.rmtree(folder_path)  
        print(f"文件夹 {folder_path} 及其所有内容已被删除。")  
    else:  
        print(f"文件夹 {folder_path} 不存在。")

    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 已成功创建。")


# 视频文件切分 理逻辑 第一段为指定长度，从第二段开始 ，起始位置前移2秒，长度依然为指定长度
def split_video(video_file, output_dir, split_length_seconds,overlap_seconds):
    """
    视频文件切分 理逻辑 第一段为指定长度，从第二段开始 ，起始位置前移2秒[重叠时间为2秒]，长度依然为指定长度
    """
    # 加载视频文件
    video = VideoFileClip(video_file)
    video_duration = int(video.duration)

    # 如果传入的路径不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 用于存储返回视频片段的路径
    return_video_paths = []

    segment = 0
    end_time = split_length_seconds
    while True:
        # 第一段保持原始逻辑不变
        if segment == 0:
            start_time = 0
        else:
            # 从第二段开始，起始时间前移2秒，但不小于0
            start_time = max(end_time - overlap_seconds, 0)

        end_time = start_time + split_length_seconds

        # 如果起始时间超过了视频总长，结束循环
        if start_time >= video_duration:
            break

        # 确保结束时间不会超出视频总时长
        end_time = min(end_time, video_duration)

        # 创建每个片段的子剪辑
        subclip = video.subclip(start_time, end_time)

        # 保存每个片段到指定的输出目录
        output_path = os.path.join(output_dir, f"segment_{segment + 1}.mp4")
        subclip.write_videofile(
            output_path, codec="libx264", audio_codec="aac")

        print(f"Segment {segment + 1} saved: {output_path}")
        return_video_paths.append(output_path)

        # 如果结束时间已经是视频的结尾，结束循环
        if end_time == video_duration:
            break

        segment += 1

    video.close()
    print("Video splitting completed.")

    return return_video_paths



# 视频文件切分，将指定视频文件按照指定的时间切分成两个视频片段
def split_video_two(video_file, output_dir, point_time_seconds):
    """

     返回值： 存储片段路径的数组
     调用样例： split_audio("input.mp3", "output_dir", 10)  # 在第10秒的位置进行切割，切割成两部分，保存到output_dir目录

    """
    # 加载视频文件
    video = VideoFileClip(video_file)
    video_duration = int(video.duration)

    # 如果传入的路径不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 用于存储返回视频片段的路径
    return_video_paths = []


    if point_time_seconds >= video_duration:
        total_segments = 1
        end_time = video_duration
    else:
        total_segments = 2
        end_time = point_time_seconds


    for segment in range(total_segments):
        if segment == 0:
            start_time = 0
        else:
            start_time = point_time_seconds
            end_time = video_duration   

        # Create a subclip for each segment
        subclip = video.subclip(start_time, end_time)

        # Save the subclip to the specified output directory
        output_path = os.path.join(output_dir, f"segment_{segment + 1}.mp4")
        subclip.write_videofile(
            output_path, codec="libx264", audio_codec="aac")

        print(f"Segment {segment + 1} saved: {output_path}")
        return_video_paths.append(output_path)

    video.close()
    print("Video splitting completed.")

    return return_video_paths


def srt_to_txt(srt_file_path, txt_file_path):
    """
    将SRT字幕文件转换为TXT文本文件。

    :param srt_file_path: SRT文件的路径。
    :param txt_file_path: 要创建的TXT文件的路径。
    """
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            lines = srt_file.readlines()

        # 提取并清理字幕文本
        text_lines = []
        for line in lines:
            # 跳过空行和仅包含数字的行（序号）
            if line.strip().isdigit() or not line.strip():
                continue
            # 跳过时间戳行
            if '-->' in line:
                continue
            # 添加非空的文本行
            text_lines.append(line.strip())

        # 写入TXT文件
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            for line in text_lines:
                txt_file.write(line + '\n')

        print(f"SRT字幕转换完成，保存在：{txt_file_path}")
    except Exception as e:
        print(f"转换失败：{e}")




def extract_subtitles(video_dir,output_dir):
    """
    字幕提取
    第一个参数是指定要提取字幕的视频的的所在路径
    第二个参数是指定输出字幕的路径
    """

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 用于存储返回视频片段的路径
    return_paths = []

    # 遍历所有视频文件进行处理
    for video_path in video_dir:
        video_file = os.path.basename(video_path)
        txt_output_path = os.path.join(output_dir, video_file.split(".")[0]+".txt")
        srt_output_path = os.path.join(output_dir, video_file.split(".")[0]+".srt")
        return_paths.append(txt_output_path)
        return_paths.append(srt_output_path)
        os.system(
                'whisper "{}" --model medium --output_format srt --output_dir {}'.format(video_path,output_dir))
        
        print(video_file + "srt字幕提取完成。。。")

        # 将srt字幕文件处理成txt字幕文件
        srt_to_txt(srt_output_path, txt_output_path)

        print(video_file + "txt字幕文件处理完成。。。")

    return return_paths



def exec_workflow():
    pass




# 自定义字符串处理器一
import re


def string_processor_01(input_text):
    """  
########################处理前##############################################
### 第一分镜：穿上设计师服装  
- **场景**: 后台化妆间，四周挂满了五光十色的灯光，设计师们忙碌地调整服装。  
- **毛球的形象**: 可爱的猫咪毛球站在化妆镜前，身穿一件精致的设计师服装，这件服装色彩斑斓，带有异域风情的图案。  
- **毛球的动作和表情**: 毛球表情稍显紧张，但也流露出一丝兴奋。它试图用爪子调整衣服上的小装饰，动作拟人化且略显笨拙，让人忍俊不禁。 

### 第四分镜：观众欢呼喝彩
- **场景**: T台的末端，聚光灯聚焦在毛球身上，背景是模糊的欢呼观众。
- **毛球的形象**: 毛球穿着本场秀的压轴服装，这件服装集设计之大成，华美而不失优雅。
- **毛球的动作和表情**: 毛球站在T台的末端，挥动爪子向观众致谢，表情是惊喜交加，尾巴摇摆频频，完全沉醉在这片刻的荣耀中。  
    


########################处理后##############################################
场景: 后台化妆间...  毛球的形象: 可爱的猫咪毛球....有异域风情的图案。  毛球的动作和表情: 毛球表情稍...让人忍俊不禁。   
场景: T台的末端...呼观众。  毛球的形象: 毛球穿着本...不失优雅。  毛球的动作和表情: 毛球...荣耀中。  
    """
    # 按照空行进行分割
    blocks = re.split(r'\n\s*\n', input_text)
    list = []
    for block in blocks:
        # 按行分割文本
        lines = block.split('\n')

        # 过滤掉以三个###开头的行
        filtered_lines = [line for line in lines if not line.startswith('###')]

        # 去除每行开头的 "处理前字符串：" 和行尾的 "-"
        processed_lines = [line.strip().replace("处理前字符串：", "").rstrip("-")
                           for line in filtered_lines]

        # 合并处理后的行成一个字符串，并去除多余的空格
        output_text = ' '.join(processed_lines).strip()

        # 添加到数组中
        list.append(output_text.replace("**", "").replace("-", "").strip())

    return list
















