from setuptools import setup, find_packages

setup(
    name='reyan',
    version='0.0.57',
    packages=find_packages(),
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'reyan = reyan.sac:sac',
        ],
    },
    author='reyan',
    description='reyan.',
    url='https://github.com/r-e-y-a-n/reyan-pip',
)
