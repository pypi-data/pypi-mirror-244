#!/usr/bin/env python
import os
from setuptools import setup, find_packages
import listen

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

# # Function to check if torch.cuda.is_available() without importing torch
# def is_cuda_available():
#     try:
#         # Attempt to import torch without actually importing it
#         from importlib import util as import_util
#         spec = import_util.find_spec('torch')
#         return spec is not None
#     except Exception:
#         return False

# # Check if GPU is available using the is_cuda_available function
# gpu_available = is_cuda_available()

dependencies = [
        #'torch', # Please install the correct version of torch manually
        'torchaudio',
        'transformers',
        'numpy>=1.15.1',
        'pyaudio>=0.2.12',
        'webrtcvad>=2.0.10',
        'scipy>=1.1.0',
        'toml>=0.10.2',
        'sanic>=22.6.0',
        'ffmpeg-python>=0.2.0',
        'websockets>=10.3',
        'deepmultilingualpunctuation',
        'pyctcdecode', # Wav2Vec2ProcessorWithLM requires the pyctcdecode library
        'kenlm', # Ironic that it doesn't work without it
        'fastapi',
        'accelerate',
    ]

setup(
    name='stt-listen',
    author='Danny Waser',
    version=listen.__version__,
    license='LICENSE',
    url='https://gitlab.com/waser-technologies/technologies/listen',
    description='Transcribe long audio files with ASR or use the streaming interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('.'),
    python_requires='>=3.8,<3.12',
    install_requires = dependencies,
    entry_points={
        'console_scripts': [
            'listen = listen.main:main',
        ]
    },
)
