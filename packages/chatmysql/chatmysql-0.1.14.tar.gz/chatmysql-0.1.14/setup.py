from setuptools import setup, find_packages
from cmysql.version import APP_VERSION

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()
    install_requires = [r.strip() for r in requirements if r.strip()]


setup(
    name='chatmysql',
    version=APP_VERSION,
    description='A simple chat cli based on mysql cli.',
    url='https://github.com/DataMini/cmysql',
    author='lele',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'chatmysql = cmysql.cli:main',
        ]
    },
    install_requires=install_requires
)
