from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PassGenCLI',
    version='0.2.0',
    author='Fathi Abdelmalek',
    author_email='abdelmalek.fathi.2001@gmail.com',
    url='https://github.com/fathiabdelmalek/PassGenCLI',
    description='Password Generator CLI use `f-passwords-generator` package.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['passgencli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
