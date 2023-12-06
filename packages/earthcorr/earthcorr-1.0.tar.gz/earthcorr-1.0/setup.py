import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = 'v1.0'
DESCRIPTION = ''

setup(
    name="earthcorr",
    version=VERSION,
    author="zhangym",
    author_email="976435584@qq.com",
    description=DESCRIPTION,
    # 长描述内容的类型设置为markdown
    #long_description_content_type="text/markdown",
    # 长描述设置为README.md的内容
    #long_description=long_description,
    # 使用find_packages()自动发现项目中的所有包
    packages=find_packages(),
    # 许可协议
    license='MIT',
    # 要安装的依赖包
    install_requires=[
        "Faker>=18.7.0",
        "ddddocr>=1.4.7",
        "requests>=2.30.0",
        "loguru>=0.7.0",
        "lxml>=4.9.2",
    ],
    # keywords=['python', 'menu', 'dumb_menu','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

