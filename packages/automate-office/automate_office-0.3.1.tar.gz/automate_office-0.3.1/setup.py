from setuptools import setup, find_packages


setup(
    name="automate_office",
    version="0.3.1",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
        "python-docx==1.1.0",
        "python-pptx==0.6.23",
        "openpyxl==3.1.2"
    ],

    author="Sun Meng",
    author_email="clivesun@163.com",
    description="Offic自动化工具-自用，在原有包的基础上二次开发, PPT部分暂时告一段落, Word暂时用处不大, Excel做了一些函数和例子",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    license="",
    url="",
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # 开发的目标用户
        "Intended Audience :: Developers",
        # 属于什么类型
        "Topic :: Software Development :: Build Tools",
        # 许可证信息
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)