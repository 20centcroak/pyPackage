import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyInstallPackage", 
    version="0.1",
    author="20centCroak",
    author_email="",
    description="Standard app packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/20centcroak/pyPackage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'PyBaseApp',
          'PyInstaller'
      ],
)