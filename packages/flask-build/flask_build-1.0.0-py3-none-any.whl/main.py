import os

import click

"""
pip install click
https://click.palletsprojects.com/en/8.1.x/
"""

"""
command 使得函数 hello 作为命令行接口；
option 添加命令行选项；
click.echo 主要是从兼容性考虑：Python2 的 print 是语句，而 Python3 中则为函数。
"""

import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello {name}!".format(name=name))


@click.command("build")
def build():
    """

    :param count:
    :param name:
    :return:
    """
    click.echo('build')

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

                 ]

    for path in path_list:
        os.makedirs(path, exist_ok=True)

    file_list = ["application/__init__.py",
                 "application/models/__init__.py",
                 "application/views/__init__.py",
                 "application/utils/__init__.py",
                 "application/dist/__init__.py",
                 "application/extensions/__init__.py",

                 ".flask_env"  # flask 配置文件
                 "gunicorn.conf.py"  # Gunicorn配置文件

                 ]

    file_content = {
        ".flask_env": "DEBUG=True",
    }
    for file in file_list:
        with open(file, "w") as f:
            f.write("")

    print("路径被创建")


if __name__ == '__main__':
    # 将命令添加到命令行工具
    command_line_tool = click.Group()
    command_line_tool.add_command(hello)
    command_line_tool.add_command(build)
    command_line_tool()

