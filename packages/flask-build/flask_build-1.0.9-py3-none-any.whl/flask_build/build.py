# encoding: utf-8
# build.py


"""
pip install click
https://click.palletsprojects.com/en/8.1.x/
"""
import shutil
import zipfile

import requests

"""
command 使得函数 hello 作为命令行接口；
option 添加命令行选项；
click.echo 主要是从兼容性考虑：Python2 的 print 是语句，而 Python3 中则为函数。

colorama 是一个用于在命令行界面上添加彩色输出的 Python 库。
它允许你在终端中使用 ANSI 转义码来添加颜色和样式，从而增强命令行的可读性。
"""
from colorama import Fore, Back, Style
import os
import sys
import click
import colorama


# 初始化 colorama，确保在 Windows 上也能正常工作
colorama.init(autoreset=True)


def get_platform():
    """
    获取系统平台

    """
    platform = sys.platform
    if platform.startswith('linux'):
        return 'Linux'
    elif platform.startswith('darwin'):
        return 'macOS'
    elif platform.startswith('win'):
        return 'Windows'


platform = get_platform()


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello {name}!".format(name=name))


@click.command("flask")
def build():
    """

    :param count:
    :param name:
    :return:
    """
    click.echo('build flask init')

    # 创建的目录
    path_list = ["application",  # 应用目录
                 "application/models",  # 数据模型目录
                 "application/views",  # 视图目录
                 "application/utils",  # 工具类
                 "application/dist",  # vue 构建目录
                 "application/extensions",  # flask扩展
                 "application/forms",  # 表单验证目录
                 "application/config",  # 配置文件目录

                 "logs",  # 日志目录
                 "logs/debug",
                 "logs/info",
                 "logs/warning",
                 "logs/error",
                 "logs/critical",

                 "scripts",  # 脚本

                 ]

    for path in path_list:
        os.makedirs(path, exist_ok=True)

    file_list = ["application/__init__.py",
                 "application/models/__init__.py",
                 "application/views/__init__.py",
                 "application/utils/__init__.py",
                 "application/dist/__init__.py",
                 "application/extensions/__init__.py",

                 ".flask_env",  # flask 配置文件
                 "gunicorn.conf.py"  # Gunicorn配置文件

                 ]


    for file in file_list:
        with open(file, "w") as f:
            f.write("")

    print(Fore.GREEN + "路径被创建")
    make_script()
    download_temple()


def main():
    command_line_tool = click.Group()
    command_line_tool.add_command(hello)
    command_line_tool.add_command(build)
    command_line_tool()


def make_script():
    if platform == "Windows":

        with open("scripts/start_server.bat", "w") as f:
            f.write("gunicorn -c gunicorn.conf.py wsgi:app")

        with open("scripts/upgrade_db.bat", "w") as f:
            content = """
            echo "开始迁移数据库..."
            flask db init
            flask db migrate -m 'xxx'
            flask db upgrade
            echo "按任意键继续..."
            pause
            """

            f.write(content)


    elif platform == "Linux":
        with open("scripts/start_server.sh", "w") as f:
            f.write("gunicorn -c gunicorn.conf.py wsgi:app")

        with open("scripts/upgrade_db.sh", "w") as f:
            content = """
            printf "开始迁移数据库..."
            flask db init
            flask db migrate -m 'xxx'
            flask db upgrade
            printf "按任意键继续..."
            """

            f.write(content)



# 下载
def download_temple():
    # 下载模板
    url = 'https://codeload.github.com/Morishima-Hodaka/flask-example/zip/refs/heads/main'

    response = requests.get(url, stream=True)
    with open("temple.zip", 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    with zipfile.ZipFile('temple.zip', 'r') as zip_ref:
        zip_ref.extractall('..')


if __name__ == '__main__':
    # 将命令添加到命令行工具
    command_line_tool = click.Group()
    command_line_tool.add_command(hello)
    command_line_tool.add_command(build)
    command_line_tool()
