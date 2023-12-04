from setuptools import setup

setup(
    name='flask-build',
    version='1.0.2',
    entry_points={
        'console_scripts': [
            'build = flask_build:build',
        ],
    }
)



