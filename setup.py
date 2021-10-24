from setuptools import setup, find_packages

setup(
    name="dgit",
    version="1.0",
    author="tonyguo",
    author_email="mymail",
    packages=find_packages(),
    # scripts=['dgit/main.py'],
    entry_points={
        'console_scripts': ['dgit=dgit.main:main'],
    }
)
