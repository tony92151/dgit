from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dgit",
    version="0.5.2",
    author="tonyguo",
    author_email="tony92151@gmail.com",
    url="https://github.com/tony92151/dgit",
    packages=find_packages(),
    # scripts=['dgit/main.py'],
    entry_points={
        'console_scripts': ['dgit=dgit.main:main'],
    },
    install_requires=[
         'GitPython>=3.1.18',
         'dvc>=2.7.4'
     ],
    python_requires=">=3.6",
)
