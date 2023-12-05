from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='umbrage_evals',
    version='0.0.1',
    packages=find_packages(),
    description='Umbrage Evals SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='umbrage.ai',
    author_email='matthew.groff@umbrage.com',
    url='https://github.com/Umbrage-Studios/umbrage-evals',
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
