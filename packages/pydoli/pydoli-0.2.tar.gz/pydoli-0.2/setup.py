# setup.py

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pydoli',
    version='0.2',
    description='A simple todo list app for the command line',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/linyers/pydoli',
    author='Linyers',
    author_email='linyers666@gmail.com',
    license='MIT',
    packages=['pydoli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
)
