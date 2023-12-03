from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as f:
    desc=f.read()

setup(
    name='regex_custom_dict',
    version='0.6',
    packages=find_packages(),
    install_requires=[],
    long_description=desc,
    long_description_content_type="text/markdown"
)
