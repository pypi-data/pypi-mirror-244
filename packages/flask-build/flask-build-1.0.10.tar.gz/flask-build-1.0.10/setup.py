from setuptools import setup

setup(
    name='flask-build',
    version='1.0.10',
    packages=['flask_build'],  # 包含的包列表，包括子包，可用find_pakages()
    entry_points={
        'console_scripts': [
            'build = flask_build:main',
        ],
    }
)



