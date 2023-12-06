from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Returns the next number'

# Setting up
setup(
    name="givesNextNumber",
    version=VERSION,
    author="Akash",
    author_email="<akash.de117@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'number'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
