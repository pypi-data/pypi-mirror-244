from setuptools import find_packages, setup

setup(
    name="super_projekt",
    version='0.0.2',
    author="Gokuruto",
    packages=find_packages(),
    include_package_data=True,
    description="nasz super projekt.",
    install_requires=[
        "PySimpleGUI==4.60.5"
    ]
)
