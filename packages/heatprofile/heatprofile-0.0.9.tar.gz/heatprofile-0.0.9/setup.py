from setuptools import setup, find_packages

setup(
    name='heatprofile',
    version='0.0.9',
    package_dir={"": "heatprofile"},
    packages=find_packages(where="heatprofile"),
    install_requires=[
        'psutil',
    ],
    # Add more metadata like author, URL, dependencies, etc.
)