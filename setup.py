from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in superstar_rides/__init__.py
from superstar_rides import __version__ as version

setup(
	name="superstar_rides",
	version=version,
	description="An app to manage vehicle rentals",
	author="Hussain",
	author_email="hussain@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
