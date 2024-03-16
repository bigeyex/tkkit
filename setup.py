from setuptools import setup, find_packages

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='tkkit',
    version='1.0.0',
    author='bigeyex',
    author_email='bigeyex@gmail.com',
    description='Write tkinter (Windows/Mac GUI) interface faster and easier',
    long_description=long_description,
    url="https://github.com/bigeyex/tkkit",
    packages=['tkkit'],
    python_requires='>=3.6',
)
