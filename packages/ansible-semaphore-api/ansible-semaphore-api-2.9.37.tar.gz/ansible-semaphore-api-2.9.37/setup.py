import os
from setuptools import setup, find_packages
from pathlib import Path

long_description = """
=====
Ansible Semaphore API
=====

API Lib allows communication with Ansible-Semaphore API.

API demo: https://www.ansible-semaphore.com/api-docs/
"""




req_file_path = Path(__file__).parent / "requirements.txt"
with open(req_file_path) as f:
    requirements = f.read().splitlines()
    
NAME = os.getenv('NAME', "ansible-semaphore-api")   
VERSION = os.getenv('SEMAPHORE_VERSION')

setup(
    name=NAME,
    version=VERSION,
    description="Ansible Semaphore Python API",
    author="Nchekwa",
    author_email="artur@nchekwa.com",
    url="https://github.com/nchekwa/ansible-semaphore-api",
    keywords=["ansible-semaphore", "ansible", "api"],
    install_requires=requirements,
    packages=find_packages(exclude=["test", "tests", "docs"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    package_data={'semaphore': ['py.typed']},
    data_files=[('', ['requirements.txt'])]
)
