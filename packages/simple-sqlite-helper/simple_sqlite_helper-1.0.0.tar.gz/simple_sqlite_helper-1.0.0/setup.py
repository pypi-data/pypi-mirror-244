from setuptools import setup

setup(
    name='simple_sqlite_helper',
    version='1.0.0',
    description='Python module for easy sqlite database management',
    author='samet-catakli',
    author_email='samet@logicarbor.com',
    url='https://api.logicarbor.com/sqlitehelper/documentation.html',
    packages=['simple_sqlite_helper'],
    install_requires=['sqlite3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
