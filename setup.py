from setuptools import setup, find_packages

setup(
    name="dgit",
    version="1.1",
    author="tonyguo",
    author_email="tony92151@gmail.com",
    packages=find_packages(),
    # scripts=['dgit/main.py'],
    entry_points={
        'console_scripts': ['dgit=dgit.main:main'],
    },
    install_requires=[
         'GitPython>=3.1.18',
         'dvc>=2.7.4'
     ]
)
