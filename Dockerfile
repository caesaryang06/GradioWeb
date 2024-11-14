# 使用官方Python运行时作为父镜像
FROM python:3.10.15

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的/app目录中
COPY . /app

# 安装requirements.txt中指定的任何所需包
RUN pip install --no-cache-dir -r requirements.txt

# 使端口80可用
EXPOSE 7860

# 定义环境变量
ENV NAME World

# 在容器启动时运行app.py
CMD ["python", "gradio_main.py"]
