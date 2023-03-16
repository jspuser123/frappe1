from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in coolapp/__init__.py
from coolapp import __version__ as version

setup(
	name="coolapp",
	version=version,
	description="first_lanch",
	author="jagan",
	author_email="asp6406",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
