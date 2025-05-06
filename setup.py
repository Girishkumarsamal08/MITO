from setuptools import setup, find_packages
import os

APP = ['Main.py']
DATA_FILES = ['Resources/.env']
OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'PyQt5',
        'speech_recognition',
        'pyaudio',
        'openai',
        'pygame',
        'selenium',
        'threading'
    ],
    'includes': [
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'pyaudio',
        'speech_recognition',
        'openai',
    ],
    'excludes': ['rubicon'],
    'resources': [
        'Data',
        'FRONTEND',
        'BACKEND',
        'WAKEWORD',
        '.env',
    ],
    'plist': {
        'NSMicrophoneUsageDescription': 'Darling needs access to your microphone to talk with you',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    name='Darling',
    version='1.0',
    author='SWAYAMGIRISH',
    packages=find_packages(),
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    include_package_data=True,
)
