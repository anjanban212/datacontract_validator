from setuptools import setup, find_packages

setup(
    name="data-contracts-validator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "pandera>=0.17.0",
        "pyyaml>=6.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "pyarrow>=14.0.0",  # For Parquet support
        "fastparquet>=2023.0.0",  # Alternative Parquet engine
    ],
    entry_points={
        "console_scripts": [
            "validate-contract=data_contracts_validator.cli:main",
        ],
    },
    author="Anjan Banerjee",
    author_email="anjanban212@gmail.com",
    description="A CLI tool for validating data against YAML-defined schema contracts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anjanban212/data-contracts-validator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 