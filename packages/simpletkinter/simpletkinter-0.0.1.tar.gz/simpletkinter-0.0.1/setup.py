import re

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

VERSION_FILE="simpletkinter/_version.py"
with open(VERSION_FILE, 'r') as f_version:
    version_string = f_version.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_string, re.M)
if mo:
    version_string = mo.group(1)
else:
    raise RuntimeError(f'Unable to find version string in {VERSION_FILE}.')


setup_args = dict(
    name='simpletkinter',
    version=version_string,
    description='"""A simple approach to some tkinter widgets."""',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='jeff watkins',
    author_email='support@bidforgame.com',
    keywords=['tkinter'],
    url='https://psionman@bitbucket.org/psionman/bfgdealer.git',
    download_url='https://pypi.org/project/bfgdealer/',
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
