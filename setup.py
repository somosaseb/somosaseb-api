from setuptools import setup, find_packages

setup(
    name="aseb-app",
    version="1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
)
