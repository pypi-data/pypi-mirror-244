import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.9'
DESCRIPTION = '瞎写一通'

setup(
    name="shadow-game-tools",
    version=VERSION,
    author="shadow",
    author_email="516043893@qq.com",
    description=DESCRIPTION,
    # 长描述内容的类型设置为markdown
    long_description_content_type="text/markdown",
    # 长描述设置为README.md的内容
    long_description=long_description,
    # 使用find_packages()自动发现项目中的所有包
    packages=find_packages(),
    # 许可协议
    license='MIT',
    # 要安装的依赖包
    install_requires=[
        'pypiwin32',
        'opencv-python',
        'rpyc'
    ],
    # keywords=['python', 'menu', 'dumb_menu','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

'''
生成分发档案：在你的包的目录下运行以下命令来生成分发档案：python setup.py sdist bdist_wheel。这将会在dist目录下生成两个文件。

上传分发档案：运行以下命令来上传分发档案到PyPI：twine upload dist/*。在这个过程中，你需要输入你在第2步中创建的PyPI账户的用户名和密码。

'''