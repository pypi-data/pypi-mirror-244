# encoding: utf-8
# build.py


"""
pip install click
https://click.palletsprojects.com/en/8.1.x/
"""


import requests

import zipfile
import shutil


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
    path_list = [

                 "scripts",  # 脚本

                 ]

    for path in path_list:
        os.makedirs(path, exist_ok=True)

    file_list = [

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

    with zipfile.ZipFile('./temple.zip', 'r') as zip_ref:
        zip_ref.extractall()

    # 获取源文件夹中的所有文件列表
    files = os.listdir('./flask-example-main')
    # 遍历文件列表并剪切到目标文件夹
    for file in files:
        path = os.path.join('./flask-example-main', file)
        shutil.move(path, '.')


if __name__ == '__main__':
    # 将命令添加到命令行工具
    command_line_tool = click.Group()
    command_line_tool.add_command(hello)
    command_line_tool.add_command(build)
    command_line_tool()
