from setuptools import setup, find_packages

setup(
    name='heatprofile',
    version='0.0.7',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'psutil',
    ],
    # Add more metadata like author, URL, dependencies, etc.
)