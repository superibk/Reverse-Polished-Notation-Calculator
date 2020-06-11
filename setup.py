from setuptools import setup

setup(
    name = 'rpn',
    version = '0.1.0',
    packages = ['rpn'],
    entry_points = {
        'console_scripts': [
            'rpn = rpn.__main__:main'
        ]
    })
