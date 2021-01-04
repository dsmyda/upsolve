
from setuptools import setup, find_packages
from upsolve.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='upsolve',
    version=VERSION,
    description='Upsolve manages and reminds you about contest problems that you weren\'t able to solve.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='dsmyda',
    author_email='danny.smyda@gmail.com',
    url='https://github.com/dsmyda/upsolve',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'upsolve': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        upsolve = upsolve.main:main
    """,
)
