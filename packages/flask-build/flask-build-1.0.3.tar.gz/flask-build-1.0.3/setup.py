from setuptools import setup

setup(
    name='flask-build',
    version='1.0.3',
    entry_points={
        'console_scripts': [
            'build = flask_build:build',
        ],
    }
)



