from setuptools import setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

setup(
    name="ProdNet",
    author="Leonardo Niccolò Ialongo, Davide Luzzati",
    author_email="leonardo.ialongo@gmail.com",
    python_requires=">=3.0",
    version="0.0.2",
    url="https://github.com/LeonardoIalongo/ProdNet",
    description=(
        "A collection of models of economic Production Networks and "
        "their associated measures and functions."
    ),
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    license="GNU General Public License v3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=["ProdNet"],
    package_dir={"": "src"},
    install_requires=["numpy>=1.22", "numba>=0.58", "scipy>=1.6"],
)
