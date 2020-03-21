from setuptools import setup, find_packages

with open('ctpl/VERSION', 'r') as ver_file:
    __version__ = ver_file.read().strip()


setup(
    name='ctpl',
    version=__version__,
    packages=find_packages(where='.'),
    install_requires=[
        'Click',
        'docxtpl'
    ],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        ctpl=ctpl.cli:ctpl
    '''
)
