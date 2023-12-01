from setuptools import find_packages, setup

with open("VERSION", "r") as f:
    VERSION = f.read().strip()

DESCIPTION = "a simple cron-job.org sdk"

with open("requirements.txt", "r") as requirements_file:
    REQUIREMENTS = requirements_file.readlines()

with open("README.md", "r") as requirements_file:
    README = requirements_file.read()

setup(
    name="pycronorg",
    version=VERSION,
    author="axdjuraev",
    author_email="<axdjuraev@gmail.com>",
    description=DESCIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)

