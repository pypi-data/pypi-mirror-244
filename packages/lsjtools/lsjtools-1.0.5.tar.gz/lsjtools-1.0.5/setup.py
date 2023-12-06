import pathlib

import setuptools

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="lsjtools",
    version="1.0.5",
    author="Linxm",
    author_email="547304723@qq.com",
    description="Python环境下的工具库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/linxm/lsjtools.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
    keywords="lsjtools",
)

# python setup.py sdist 进行打包
# twine upload dist/* 发布到pypi

# [pypi]
# username = __token__
# password = pypi-AgEIcHlwaS5vcmcCJDYwZjU5MzliLWQzN2YtNDA4Yy1iYWM0LTNmMGFhZWU3NTMzZQACKlszLCJmZGVkYTUwYS1iODBjLTRlNGMtYjdkYS1kZDcwNzY2YTllNWQiXQAABiA8wDsfV710tgQZj6GhansTpBJ0jk4m3E211avFhlz2wg
