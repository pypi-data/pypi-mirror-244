from setuptools import find_packages, setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mikrotikrscparser',
    version='0.0.1',
    packages=find_packages(include=['mikrotikrscparser'], exclude=['tests*']),
    url='https://github.com/muqiuq/mikrotikrscparser',
    license='MIT',
    description='MikroTik RSC file parser library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={"": ["LICENSE"]},
    author='Philipp Albrecht',
    author_email='philipp@uisa.ch',
)
