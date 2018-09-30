import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certbothook",
    version="0.0.1",
    author="James McDonald",
    author_email="james@jamesmcdonald.com",
    description="A deploy hook for certbot to run a handler on renewal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamesmcdonald/certbothook",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
