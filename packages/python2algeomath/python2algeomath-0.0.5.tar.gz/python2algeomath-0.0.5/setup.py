import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python2algeomath",  # Replace with your own username
    version="0.0.5",
    author="KimKyuBong",
    author_email="tfm0405@gmail.com",
    description="to be helpful python code for Math Teacher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimkyubong/python2algeomath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
