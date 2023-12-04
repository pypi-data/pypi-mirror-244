from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='kdtest',
    version='1.1.6',
    keywords='kdtest selenium request',
    description='A keyword-driven automated testing framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url='https://gitee.com/wang_qiao123/kdtest.git',
    author='Qiao Wang',
    author_email='1603938216@qq.com',
    classifiers=[
        "Programming Language :: Python :: 3",  # 使用Python3
        "License :: OSI Approved :: Apache Software License",  # 开源协议
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'colorama==0.4.4',
        'dominate==2.6.0',
        'pipreqs==0.4.11',
        'selenium==3.141.0',
        'msedge-selenium-tools==3.141.4',
        'requests==2.27.1',
        'Eel==0.15.2',
        'openpyxl>=3.0.7',
        'pywinauto>=0.6.8',
        'ruamel.yaml>=0.17.21',
        'tqdm>=4.63.0'
    ],
    entry_points={
        "console_scripts": [
            "kdtest = kdtest.run:run"
        ]
    }
)