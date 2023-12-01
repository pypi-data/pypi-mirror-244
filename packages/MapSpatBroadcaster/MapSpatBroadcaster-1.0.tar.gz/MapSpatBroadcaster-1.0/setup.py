from setuptools import setup, find_packages
setup(
    name='MapSpatBroadcaster',
    version='1.0',
    author='Samuel Cornejo',
    author_email='samuelcornejo@arizona.edu',
    description='MAP-SPaT broadcaster classes and methods for MMITSS MRP',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)