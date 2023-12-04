from setuptools import setup

setup(
    name='flask-build',
    version='1.0.5',
    entry_points={
        'console_scripts': [
            'build = flask_build:main',
        ],
    }
)



