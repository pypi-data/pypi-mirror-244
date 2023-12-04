from time import time
import os

import setuptools
# c:\Python38\python.exe setup.py clean --all
# c:\Python38\python.exe setup.py sdist
# c:\Python38\python.exe -m build
# c:\Python38\python.exe -m twine upload dist/* --skip-existing
# 用户名 jerry1979

module_dir = os.path.dirname(__file__)

# with open('design.md', "r", encoding="utf-8") as fh:
# long_description = fh.read()

setuptools.setup(
    name="pyBeCool",
    version="1.0.0",
    author="jerry",
    author_email="6018421@qq.com",
    description="An EntityFramework+WebAPI for python, Based on Peewee and FastAPI.",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyBeCool"},
    packages=setuptools.find_packages(where="pyBeCool"),
    python_requires=">=3.8",
)
