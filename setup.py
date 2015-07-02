import sys
from setuptools import setup

if sys.version_info[:2] < (3, 1):
    sys.exit('raven-bash requires Python 3.1 or higher.')

setup(
    name='raven-bash',
    version='0.1',
    description='Raven Sentry client for Bash.',
    long_description='Sentry client for Bash. Logs errors from your bash scripts.',
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
    install_requires=['raven>=5.1.1'],
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
