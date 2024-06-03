from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='Agentic Employment',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'twine',
        'setuptools',
        'wheel',
        'flake8',
        'black',
        'pytest',
        'pip-upgrader',
        'fastapi',
        'uvicorn',
        'python-dotenv',
    ],
    author='rUv',
    author_email='null@ruv.net',
    description='an Agentic Employment Infrastructure',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ruvnet/agentic-employment',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'agentic-employment=agentic_employment_wrapper:main',
        ],
    },
)
