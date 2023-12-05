# Copyright (C) 2023 Haitao Zhou. All rights reserved.
from setuptools import setup

setup(
    name='marvolo',
    version='v0.1.2',
    description='Some useful tools about CV develeped by Marvolo',
    platforms=['all'],
    author='Marvolo',
    author_email='18377221@buaa.edu.cn',
    python_requires='>=3.6',
    url='',
    install_requires=['opencv-python','imageio', 'colorlog', 'numpy'],
    license='MIT',
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
