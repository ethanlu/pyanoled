#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="pyanoled",
    version="1.0.0",
    author="Ethan Lu",
    author_email="fang.lu@gmail.com",
    description="Python Piano LED Visualizer",
    keywords="",
    url="https://github.com/ethanlu/pyanoled",
    download_url="https://github.com/ethanlu/pyanoled",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    include_package_data=True,
    data_files=[],
    dependency_links=[],
    install_requires=[
        "argparse",
        "mido",
        "numpy",
        "Pillow",
        "psutil",
        "pyhocon",
        "python-rtmidi",
        "RPi.GPIO",
        "rpi-ws281x",
        "spidev",
        "webcolors",
        "wheel"
    ],
    tests_require=[],
    cmdclass={},
    entry_points={}
)
