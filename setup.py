# setup.py

from setuptools import setup, find_packages

setup(
    name='convert_py_cpp',
    version='0.1.0',
    description='A library to convert Python code to C++',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kesballo',
    author_email='kesballot@gmail.com',
    url='https://github.com/kesballoReal/convert_py_cpp',
    packages=find_packages(include=['app', 'app.converter', 'app.converter.src']),
    install_requires=[
        
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'convert=app.converter.src.converter:convert',  
        ],
    },
)
