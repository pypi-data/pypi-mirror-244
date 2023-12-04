from setuptools import setup

setup(
    name='flask-build',
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'build = build:build',
        ],
    }
)



