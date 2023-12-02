import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mixinsdk",
    version="0.2.1",
    author="nodewee",
    author_email="nodewee@gmail.com",
    description="python sdk for mixin: https://github.com/nodewee/mixin-sdk-python",
    keywords=["mixin", "python", "sdk", "api", "mixin network"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nodewee/mixin-sdk-python",
    project_urls={
        "Github Repo": "https://github.com/nodewee/mixin-sdk-python",
        "Bug Tracker": "https://github.com/nodewee/mixin-sdk-python/issues",
        "About Mixin": "https://developers.mixin.one/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["examples"]),
    python_requires=">=3.9",
    install_requires=[
        "requests",
        "pyjwt",
        "cryptography",
        "pynacl",
        "httpx",
        "websockets",
        "dacite",
    ],
)
