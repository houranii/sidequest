from setuptools import find_packages, setup

setup(
    name='hometask_rev',
    version='0.1',
    description='A Flask application for handling user birthdays',
    author='Ahmad Hourani',
    author_email='ahmed.hourani@gmail.com',
    url='https://github.com/houranii/hometask_rev',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0',
        'redis>=4.0',
        'prometheus-flask-exporter>=0.18.1',
        'flask-cors>=3.0.10',
        'unittest2',
        'mock>=4.0',
    ],
    extras_require={
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.10',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)