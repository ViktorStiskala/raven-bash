import sys
from setuptools import setup

long_description = '''\
Raven Sentry client for Bash.

Logs error if one of your commands exits with non-zero return code and produces simple traceback for
easier debugging. It also tries to extract last values of the variables visible in the traceback.
Environment variables and stderr output are also included.

For more information please visit project repo on GitHub: https://github.com/hareevs/raven-bash
'''


setup(
    name='raven-bash',
    version='0.1.1',
    description='Raven Sentry client for Bash.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='raven sentry bash',
    author='Viktor Stískala',
    author_email='viktor@stiskala.cz',
    url='https://github.com/hareevs/raven-bash',
    license='Apache License 2.0',
    install_requires=['raven>=5.1.1', 'configparser'],
    packages=['logger'],
    package_data={'logger': ['raven-bash', 'logger/*.py']},
    entry_points={
        'console_scripts': [
            'raven-logger=logger.raven_logger:main',
        ],
    },
    scripts=['raven-bash'],
    zip_safe=False
)
