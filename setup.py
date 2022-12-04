from setuptools import setup

setup(
    name='logToTopo',
    version='1.0.0',
    description='A simple topology generation tool',
    long_description='A tool to generate a topology from the output of show router inteface command.',
    long_description_content_type='text/x-rst',
    url='https://github.com/laimaretto/logToTopo',
    author='Lucas Aimaretto',
    author_email='laimaretto@gmail.com',
    license='BSD 3-clause',
    packages=['src/taskAutom'],
    install_requires=['pandas==1.5.2',
                      'pyvis==0.3.1',
                      ],
    python_requires='>=3.8',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['logToTopo=src.logToTopo.logToTopo:main'],
    },
)