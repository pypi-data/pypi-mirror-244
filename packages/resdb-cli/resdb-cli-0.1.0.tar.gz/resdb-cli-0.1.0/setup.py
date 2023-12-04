from setuptools import setup, find_packages

setup(
    name='resdb-cli',
    version='0.1.0',
    author='Gopal Nambiar',
    author_email='gnambiar@ucdavis.com',
    description='ResilientDB CLI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)