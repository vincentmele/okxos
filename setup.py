from setuptools import setup, find_packages

setup(
    name="okxos",
    version="0.1.3",
    author="Vincent Mele",
    author_email="vince@otranto.mc",
    description="A Python client for OKX OS APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vincentmele/okxos",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)