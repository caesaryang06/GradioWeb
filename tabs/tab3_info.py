import whisper
import gradio as gr

# 加载Whisper模型
model = whisper.load_model("large-v3-turbo")


def transcribe_audio(audio):
    # 使用Whisper进行语音识别
    result = model.transcribe(audio)
    return result["text"]


def func():
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["upload", "microphone"], type="filepath")
            submit_btn = gr.Button("开始识别",variant="primary")
        with gr.Column():
            text_output = gr.Textbox(label="识别结果")

    # 设置提交点击事件
    submit_btn.click(fn=transcribe_audio,
                     inputs=audio_input, outputs=text_output)
