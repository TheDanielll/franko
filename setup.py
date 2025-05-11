from setuptools import setup, find_packages

def get_version():
    with open("Franko/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    raise RuntimeError("Unable to find version string.")


setup(
    name="Franko",
    version=get_version(),
    packages=find_packages(),
    package_data={
        'Franko': ['decline.bundle.js'],
    },
    install_requires=["setuptools>=61.0", "wheel"],
    extras_require={
        'dev_deps ': [
            'pytest'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    description="A project for adding an information block to an MS .docx file",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Danila Aleksandrov",
    author_email="danila.alexandrov24@gmail.com",
    python_requires='>=3.10',
)