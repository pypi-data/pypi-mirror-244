from setuptools import setup, find_packages


with open("README.rst", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="aerarium",
    version="1.0.0",
    author="SNG Viraj Reddy",
    author_email="vir200319@gmail.com",
    description="A CLI tool to track finances",
    long_description=long_description,
    license="MIT",
    url="https://github.com/virajsazzala/aerarium",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "tabulate",
        "colorama",
        "pandas",
        "scikit-learn",
    ],
    scripts=["scripts/aerarium"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
